import pytest
from django.db.utils import IntegrityError

from ..models import (Category, Favorite, Ingredient, IngredientUnit,
                               Recipe, RecipeIngredient, Review, Step)
from .factories import (CategoryFactory, FavoriteFactory,
                                        IngredientFactory, RecipeFactory,
                                        RecipeIngredientFactory, ReviewFactory,
                                        StepFactory, UserFactory)


# ==========================================================
# Category
# ==========================================================
@pytest.mark.django_db
def test_create_category():
    category = CategoryFactory()

    assert category.name.startswith("Category")
    assert category.slug.startswith("category-")


@pytest.mark.django_db
def test_create_multiple_categories():
    category1 = CategoryFactory()
    category2 = CategoryFactory()

    assert category1 != category2
    assert category1.slug != category2.slug


@pytest.mark.django_db
def test_category_slug_is_unique():
    Category.objects.create(
        name="Dessert",
        slug="dessert",
    )

    with pytest.raises(IntegrityError):
        Category.objects.create(
            name="Cake",
            slug="dessert",
        )


@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(
        name="Dessert",
        slug="dessert",
    )

    assert str(category) == "Dessert"


# ==========================================================
# User
# ==========================================================
@pytest.mark.django_db
def test_create_user():
    user = UserFactory()

    assert user.username.startswith("user")
    assert user.email.endswith("@example.com")


@pytest.mark.django_db
def test_user_password_is_hashed():
    user = UserFactory()

    assert user.check_password("password123")


# ==========================================================
# Ingredient
# ==========================================================
@pytest.mark.django_db
def test_create_ingredient():
    ingredient = IngredientFactory()

    assert ingredient.name.startswith("Ingredient")


@pytest.mark.django_db
def test_create_multiple_ingredients():
    ingredient1 = IngredientFactory()
    ingredient2 = IngredientFactory()

    assert ingredient1 != ingredient2
    assert ingredient1.name != ingredient2.name


@pytest.mark.django_db
def test_ingredient_name_is_unique():
    Ingredient.objects.create(
        name="Sugar",
    )

    with pytest.raises(IntegrityError):
        Ingredient.objects.create(
            name="Sugar",
        )


@pytest.mark.django_db
def test_ingredient_str():
    ingredient = Ingredient.objects.create(
        name="Sugar",
    )

    assert str(ingredient) == "Sugar"


# ==========================================================
# Recipe
# ==========================================================
@pytest.mark.django_db
def test_create_recipe():
    recipe = RecipeFactory()

    assert recipe.title.startswith("Recipe")
    assert recipe.category is not None
    assert recipe.author is not None


@pytest.mark.django_db
def test_recipe_slug_is_generated():
    recipe = Recipe.objects.create(
        title="Best Pizza",
        description="Very tasty",
        cooking_time=30,
        category=CategoryFactory(),
        author=UserFactory(),
    )

    assert recipe.slug == "best-pizza"


@pytest.mark.django_db
def test_recipe_category():
    category = CategoryFactory(name="Dessert")

    recipe = RecipeFactory(
        category=category,
    )

    assert recipe.category == category


@pytest.mark.django_db
def test_recipe_author():
    user = UserFactory()

    recipe = RecipeFactory(
        author=user,
    )

    assert recipe.author == user


@pytest.mark.django_db
def test_recipe_str():
    recipe = RecipeFactory(
        title="Pizza",
    )

    assert str(recipe) == "Pizza"


@pytest.mark.django_db
def test_recipe_ordering():
    RecipeFactory(title="B Recipe")
    RecipeFactory(title="A Recipe")
    RecipeFactory(title="C Recipe")

    recipes = list(Recipe.objects.all())

    assert recipes[0].title == "A Recipe"
    assert recipes[1].title == "B Recipe"
    assert recipes[2].title == "C Recipe"


# ==========================================================
# RecipeIngredient
# ==========================================================
@pytest.mark.django_db
def test_create_recipe_ingredient():
    recipe_ingredient = RecipeIngredientFactory()

    assert recipe_ingredient.recipe is not None
    assert recipe_ingredient.ingredient is not None
    assert recipe_ingredient.amount > 0
    assert recipe_ingredient.unit == IngredientUnit.GRAM


@pytest.mark.django_db
def test_recipe_ingredient_str():
    recipe = RecipeFactory(title="Pizza")
    ingredient = IngredientFactory(name="Cheese")

    recipe_ingredient = RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=200,
        unit=IngredientUnit.GRAM,
    )

    assert str(recipe_ingredient) == "Pizza - Cheese"


@pytest.mark.django_db
def test_recipe_ingredient_relationship():
    recipe = RecipeFactory()
    ingredient = IngredientFactory()

    recipe_ingredient = RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=100,
        unit=IngredientUnit.GRAM,
    )

    assert recipe_ingredient.recipe == recipe
    assert recipe_ingredient.ingredient == ingredient


@pytest.mark.django_db
def test_recipe_ingredient_is_unique():
    recipe = RecipeFactory()
    ingredient = IngredientFactory()

    RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=100,
        unit=IngredientUnit.GRAM,
    )

    with pytest.raises(IntegrityError):
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=200,
            unit=IngredientUnit.GRAM,
        )


@pytest.mark.django_db
def test_recipe_ingredient_ordering():
    recipe = RecipeFactory()

    cheese = IngredientFactory(name="Cheese")
    tomato = IngredientFactory(name="Tomato")

    RecipeIngredientFactory(
        recipe=recipe,
        ingredient=tomato,
    )

    RecipeIngredientFactory(
        recipe=recipe,
        ingredient=cheese,
    )

    recipe_ingredients = list(RecipeIngredient.objects.all())

    assert recipe_ingredients[0].ingredient.name == "Cheese"
    assert recipe_ingredients[1].ingredient.name == "Tomato"


# ==========================================================
# Step
# ==========================================================
@pytest.mark.django_db
def test_create_step():
    step = StepFactory()

    assert step.recipe is not None
    assert step.order == 1
    assert step.instruction


@pytest.mark.django_db
def test_step_str():
    recipe = RecipeFactory(title="Pizza")

    step = Step.objects.create(
        recipe=recipe,
        order=1,
        instruction="Bake",
    )

    assert str(step) == "Pizza - Step 1"


@pytest.mark.django_db
def test_step_order_is_unique():
    recipe = RecipeFactory()

    Step.objects.create(
        recipe=recipe,
        order=1,
        instruction="Step 1",
    )

    with pytest.raises(IntegrityError):
        Step.objects.create(
            recipe=recipe,
            order=1,
            instruction="Another Step",
        )


@pytest.mark.django_db
def test_step_ordering():
    recipe = RecipeFactory()

    StepFactory(
        recipe=recipe,
        order=2,
    )

    StepFactory(
        recipe=recipe,
        order=1,
    )

    steps = list(Step.objects.all())

    assert steps[0].order == 1
    assert steps[1].order == 2


# ==========================================================
# Review
# ==========================================================
@pytest.mark.django_db
def test_create_review():
    review = ReviewFactory()

    assert review.recipe is not None
    assert review.user is not None
    assert 1 <= review.rating <= 5


@pytest.mark.django_db
def test_review_str():
    user = UserFactory(username="Olivia")
    recipe = RecipeFactory(title="Pizza")

    review = Review.objects.create(
        recipe=recipe,
        user=user,
        rating=5,
        comment="Excellent",
    )

    assert str(review) == "Olivia → Pizza"


@pytest.mark.django_db
def test_review_is_unique():
    recipe = RecipeFactory()
    user = UserFactory()

    Review.objects.create(
        recipe=recipe,
        user=user,
        rating=5,
        comment="Good",
    )

    with pytest.raises(IntegrityError):
        Review.objects.create(
            recipe=recipe,
            user=user,
            rating=4,
            comment="Again",
        )


@pytest.mark.django_db
def test_review_ordering():
    review1 = ReviewFactory()
    review2 = ReviewFactory()

    reviews = list(Review.objects.all())

    assert reviews[0].created_at >= reviews[1].created_at


# ==========================================================
# Favorite
# ==========================================================
@pytest.mark.django_db
def test_create_favorite():
    favorite = FavoriteFactory()

    assert favorite.recipe is not None
    assert favorite.user is not None


@pytest.mark.django_db
def test_favorite_str():
    user = UserFactory(username="Olivia")
    recipe = RecipeFactory(title="Pizza")

    favorite = Favorite.objects.create(
        user=user,
        recipe=recipe,
    )

    assert str(favorite) == "Olivia ❤️ Pizza"


@pytest.mark.django_db
def test_favorite_is_unique():
    recipe = RecipeFactory()
    user = UserFactory()

    Favorite.objects.create(
        recipe=recipe,
        user=user,
    )

    with pytest.raises(IntegrityError):
        Favorite.objects.create(
            recipe=recipe,
            user=user,
        )


@pytest.mark.django_db
def test_favorite_ordering():
    favorite1 = FavoriteFactory()
    favorite2 = FavoriteFactory()

    favorites = list(Favorite.objects.all())

    assert favorites[0].created_at >= favorites[1].created_at
