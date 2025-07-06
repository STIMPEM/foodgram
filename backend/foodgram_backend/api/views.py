from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from django.views import View

from rest_framework import (
    status, viewsets, permissions, filters
)
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.permissions import CurrentUserOrAdminOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import (
    Ingredient,
    Recipe,
    Favorite,
    ShoppingCart,
    RecipeIngredient,
)
from users.models import Subscription

from .serializers import (
    RecipeShortSerializer,
    UserSerializer,
    AvatarSerializer,
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeDetailSerializer,
    AuthorWithRecipesSerializer,
)
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeCustomFilter, IngredientNameSearchFilter
from .utils import generate_shopping_list_content


User = get_user_model()


class UserViewSet(DjoserUserViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [CurrentUserOrAdminOrReadOnly]

    @action(
        methods=['put', 'delete'],
        detail=False,
        url_path='me/avatar',
        permission_classes=[permissions.IsAuthenticated],
        parser_classes=[JSONParser]
    )
    def avatar(self, request, *args, **kwargs):
        current_user = request.user
        if request.method == 'PUT':
            serializer = AvatarSerializer(current_user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_serializer = AvatarSerializer(current_user, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        if current_user.avatar:
            current_user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        request_author = get_object_or_404(User, id=id)
        current_user = request.user
        if request.method == 'POST':
            if current_user == request_author:
                return Response({'errors': 'Вы не можете подписываться на самого себя.'}, status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(subscriber=current_user, author=request_author).exists():
                return Response({'errors': 'Вы уже подписаны на этого пользователя.'}, status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(subscriber=current_user, author=request_author)
            response_serializer = AuthorWithRecipesSerializer(request_author, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(Subscription, subscriber=current_user, author=request_author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        current_user = request.user
        queryset = User.objects.filter(subscribers__subscriber=current_user).prefetch_related('recipe_author')
        page = self.paginate_queryset(queryset)
        serializer = AuthorWithRecipesSerializer(page if page is not None else queryset, many=True, context={'request': request})
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = [IngredientNameSearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):


    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RecipeCustomFilter

    def get_serializer_class(self, *args, **kwargs):


        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeDetailSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self._manage_user_recipe_relation(request, pk, Favorite)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self._manage_user_recipe_relation(request, pk,
                                                 ShoppingCart)

    def _manage_user_recipe_relation(self, request, pk, model):
        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        relation_exists = model.objects.filter(user=current_user, recipe=recipe).exists()
        verbose_name_plural = model._meta.verbose_name_plural.lower()
        if request.method == 'POST':
            if relation_exists:
                return Response({'errors': f'Рецепт уже добавлен в {verbose_name_plural}'}, status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(user=current_user, recipe=recipe)
            response_serializer = RecipeShortSerializer(recipe, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        if not relation_exists:
            return Response({'errors': f'Рецепта с таким ID нет в {verbose_name_plural}'}, status=status.HTTP_400_BAD_REQUEST)
        model.objects.filter(user=current_user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        current_user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=current_user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            total_amount=Sum('amount')
        ).order_by('ingredient__name')
        content = generate_shopping_list_content(ingredients)
        response = FileResponse(content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response
