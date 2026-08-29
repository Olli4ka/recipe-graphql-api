from decimal import Decimal

import factory

from ..models import (
    Category,
    Favorite,
    Ingredient,
    IngredientUnit,
    Recipe,
    RecipeIngredient,
    Review,
    Step,
    User,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    #        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall(
        "set_password",
        "password123",
    )


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Sequence(lambda n: f"Ingredient {n}")


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    title = factory.Sequence(lambda n: f"Recipe {n}")

    description = factory.Faker("paragraph")

    cooking_time = factory.Faker(
        "random_int",
        min=10,
        max=180,
    )

    category = factory.SubFactory(CategoryFactory)

    author = factory.SubFactory(UserFactory)


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    recipe = factory.SubFactory(RecipeFactory)

    ingredient = factory.SubFactory(IngredientFactory)

    amount = factory.LazyFunction(lambda: Decimal("100.00"))

    unit = IngredientUnit.GRAM


class StepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Step

    recipe = factory.SubFactory(RecipeFactory)

    order = factory.Sequence(lambda n: n + 1)

    instruction = factory.Faker("paragraph")


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    recipe = factory.SubFactory(RecipeFactory)

    user = factory.SubFactory(UserFactory)

    rating = factory.Faker(
        "random_int",
        min=1,
        max=5,
    )

    comment = factory.Faker("sentence")


class FavoriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    recipe = factory.SubFactory(RecipeFactory)

    user = factory.SubFactory(UserFactory)
