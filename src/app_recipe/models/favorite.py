from django.conf import settings
from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.PROTECT,
        related_name="favorites",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user} ❤️ {self.recipe}"
