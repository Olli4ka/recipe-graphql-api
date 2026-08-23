from django.db import models


class Step(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.PROTECT,
        related_name="steps",
    )
    order = models.PositiveIntegerField()
    instruction = models.TextField()

    class Meta:
        ordering = ["recipe", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "order"],
                name="unique_step_order",
            )
        ]

    def __str__(self):
        return f"{self.recipe} - Step {self.order}"
