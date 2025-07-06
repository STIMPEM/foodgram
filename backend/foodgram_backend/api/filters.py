import django_filters
from recipes.models import Recipe
from rest_framework import filters as rest_filters
import logging

from users.models import User

logger = logging.getLogger(__name__)


class RecipeCustomFilter(django_filters.rest_framework.FilterSet):

    author = django_filters.rest_framework.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='author'
    )
    is_favorited = django_filters.rest_framework.BooleanFilter(
        method='get_favorite_recipes'
    )
    is_in_shopping_cart = django_filters.rest_framework.BooleanFilter(
        method='get_shopping_cart_recipes'
    )

    class Meta:
        model = Recipe
        fields = ['author']

    def get_favorite_recipes(self, queryset, field_name, filter_value):
        user = self.request.user
        logger.debug(f"get_favorite_recipes: user={user}, authenticated={user.is_authenticated}, filter_value={filter_value}")
        if user.is_authenticated:
            if filter_value:
                return queryset.filter(favorites__user=user)
            else:
                return queryset.exclude(favorites__user=user)
        return queryset

    def get_shopping_cart_recipes(self, queryset, field_name, filter_value):
        user = self.request.user
        logger.debug(f"get_shopping_cart_recipes: user={user}, authenticated={user.is_authenticated}, filter_value={filter_value}")
        if user.is_authenticated:
            if filter_value:
                return queryset.filter(shopping_cart__user=user)
            else:
                return queryset.exclude(shopping_cart__user=user)
        return queryset


class IngredientNameSearchFilter(rest_filters.SearchFilter):

    search_param = "name"