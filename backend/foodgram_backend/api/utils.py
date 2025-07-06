import string
from datetime import datetime


BASE62_ALPHABET = string.digits + string.ascii_letters
BASE = len(BASE62_ALPHABET)


def generate_shopping_list_content(ingredients_queryset, recipes_info=None):

    date_str = datetime.now().strftime('%d.%m.%Y %H:%M')
    header = f'Список покупок\nДата составления: {date_str}\n'
    if not ingredients_queryset:
        return f'{header}Ваш список пуст.'
    products = []
    for idx, item in enumerate(ingredients_queryset, 1):
        name = item['ingredient__name'].capitalize()
        unit = item['ingredient__measurement_unit']
        total_amount = item['total_amount']
        products.append(f"{idx}. {name} ({unit}) — {total_amount}")
    result_parts = [header, 'Товары:', *products]
    if recipes_info:
        recipes_section = ['\nРецепты, для которых нужны эти продукты:']
        for idx, item in enumerate(ingredients_queryset, 1):
            name = item['ingredient__name']
            recs = recipes_info.get(name)
            if recs:
                recipes_list = ', '.join([f'"{r}" (автор: {a})' for r, a in recs])
                recipes_section.append(f"{idx}. {name.capitalize()}: {recipes_list}")
        result_parts.extend(recipes_section)
    return '\n'.join(result_parts)
