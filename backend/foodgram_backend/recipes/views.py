from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from .models import Recipe

def recipe_short_link(request, short_id):
    try:
        recipe_id = int(short_id)
    except (ValueError, TypeError):
        raise ValidationError('Некорректный идентификатор рецепта')
    if not Recipe.objects.filter(id=recipe_id).exists():
        raise ValidationError('Рецепт не найден')
    return redirect(f'/recipes/{recipe_id}/')
