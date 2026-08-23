from django.core.validators import MinValueValidator
from django.db import models

from .ingredient import IngredientUnit


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.PROTECT,
        related_name="recipe_ingredients",
    )

    ingredient = models.ForeignKey(
        "Ingredient",
        on_delete=models.PROTECT,
        related_name="ingredient_recipes",
    )

    amount = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    unit = models.CharField(
        max_length=10,
        choices=IngredientUnit.choices,
    )

    class Meta:
        ordering = ["recipe", "ingredient"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"
