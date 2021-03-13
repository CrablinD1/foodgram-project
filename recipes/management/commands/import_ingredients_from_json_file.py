"""Import json data from JSON file to Datababse."""
import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def import_ingredients_from_file(self, filename: str):
        with open(filename) as data_file:
            data = json.loads(data_file.read())
            for data_object in data:
                title = data_object.get("title")
                dimension = data_object.get("dimension")

                try:
                    ingredient, created = Ingredient.objects.get_or_create(
                        title=title, dimension=dimension
                    )
                    if created:
                        ingredient.save()
                        display_format = "\nIngredient, {}, has been saved."
                        print(display_format.format(ingredient))
                except Exception as ex:
                    print(str(ex))
                    msg = "\n\nSomething went wrong saving this ingredient: \
                        {}\n{}".format(
                        title, str(ex)
                    )
                    print(msg)

    def handle(self, *args, **options):
        """Call the function to import data."""
        self.import_ingredients_from_file("ingredients.json")
