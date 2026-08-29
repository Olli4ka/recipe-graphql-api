from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        max_length=255,
        blank=True,
    )
    description = models.TextField()
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredient",
        related_name="recipes",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="recipes",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
