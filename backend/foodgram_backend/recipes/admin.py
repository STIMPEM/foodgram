from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import (
    Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart
)


class BaseAdminSettings(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_per_page = 20


@admin.register(Ingredient)
class IngredientAdmin(BaseAdminSettings):
    list_display = ('name', 'measurement_unit', 'recipes_count')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)

    @admin.display(description='Число рецептов')
    def recipes_count(self, ingredient):
        return ingredient.recipes.count()


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('ingredient', 'amount')
    autocomplete_fields = ('ingredient',)
    extra = 1
    min_num = 1
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты рецепта'


@admin.register(Recipe)
class RecipeAdmin(BaseAdminSettings):
    list_display = (
        'id', 'name', 'cooking_time', 'author', 'favorites_count', 'get_ingredients_list', 'get_image_preview'
    )
    readonly_fields = ('get_image_preview', 'favorites_count')
    search_fields = ('name', 'author__username')
    list_filter = ('author', 'name')  # Changed from recipe_author to author
    inlines = [RecipeIngredientInline]
    ordering = ('-pub_date',)

    # Rest of the methods remain the same
    @admin.display(description='Первью изображения')
    def get_image_preview(self, recipe):
        if recipe.image:
            return format_html(
                '<img src="{}" width="80" height="50" />', recipe.image.url
            )
        return "Нет изображения"

    @admin.display(description='В избранном (раз)', ordering='favorited_by__count')
    def favorites_count(self, recipe):
        return recipe.favorited_by.count()

    @admin.display(description='Продукты')
    def get_ingredients_list(self, recipe):
        recipe_ingredients = recipe.recipe_ingredients.select_related('ingredient').all()
        html = '<ul>' + ''.join(
            f'<li>{ingredient.ingredient.name} — {ingredient.amount} {ingredient.ingredient.measurement_unit}</li>' 
            for ingredient in recipe_ingredients
        ) + '</ul>'
        return mark_safe(html)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')  # Changed from current_user to user
    search_fields = ('user__username', 'recipe__name')  # Changed from current_user to user
    list_filter = ('user', 'recipe')  # Changed from current_user to user
    ordering = ('id',)
    autocomplete_fields = ('user', 'recipe')  # Changed from current_user to user


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')  # Changed from current_user to user
    search_fields = ('user__username', 'recipe__name')  # Changed from current_user to user
    list_filter = ('user', 'recipe')  # Changed from current_user to user
    ordering = ('id',)
    autocomplete_fields = ('user', 'recipe')  # Changed from current_user to user