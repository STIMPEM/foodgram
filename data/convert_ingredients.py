import json

def convert_to_fixture(input_file, output_file):
    # Read the original JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        ingredients = json.load(f)

    # Convert to Django fixture format
    fixture_data = []
    for index, ingredient in enumerate(ingredients, start=1):
        fixture_item = {
            "model": "recipes.ingredient",
            "pk": index,
            "fields": {
                "name": ingredient["name"],
                "measurement_unit": ingredient["measurement_unit"]
            }
        }
        fixture_data.append(fixture_item)

    # Write the fixture file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, ensure_ascii=False, indent=2)

# Usage
input_file = 'ingredients.json'
output_file = 'ingredients_fixture.json'
convert_to_fixture(input_file, output_file)