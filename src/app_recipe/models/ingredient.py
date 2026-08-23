from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class IngredientUnit(models.TextChoices):
    GRAM = "g", "Gram"
    KILOGRAM = "kg", "Kilogram"
    MILLILITER = "ml", "Milliliter"
    LITER = "l", "Liter"
    TEASPOON = "tsp", "Teaspoon"
    TABLESPOON = "tbsp", "Tablespoon"
    CUP = "cup", "Cup"
    PIECE = "pcs", "Piece"
