import pytest

from ..models import IngredientUnit
from .factories import (
    FavoriteFactory,
    IngredientFactory,
    RecipeFactory,
    RecipeIngredientFactory,
    ReviewFactory,
    StepFactory
)


@pytest.mark.django_db
def test_recipes_query(graphql_client):
    RecipeFactory.create_batch(3)

    query = """
    query {
      recipes {
        totalCount
        items {
          title
        }
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": query},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    assert data["data"]["recipes"]["totalCount"] == 3
    assert len(data["data"]["recipes"]["items"]) == 3


@pytest.mark.django_db
def test_recipe_by_slug_query(graphql_client):
    recipe = RecipeFactory(title="Cheesecake")

    query = f"""
    query {{
      recipe(slug: "{recipe.slug}") {{
        title
        slug
        description
      }}
    }}
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": query},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    assert data["data"]["recipe"]["title"] == "Cheesecake"
    assert data["data"]["recipe"]["slug"] == recipe.slug


@pytest.mark.django_db
def test_recipe_by_slug_not_found(graphql_client):
    query = """
    query {
      recipe(slug: "recipe-does-not-exist") {
        title
      }
    }
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": query},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200

    assert "errors" in data
    assert (
        "Recipe with slug 'recipe-does-not-exist' was not found."
        in data["errors"][0]["message"]
    )


@pytest.mark.django_db
def test_recipe_with_category_and_author_query(graphql_client):
    recipe = RecipeFactory(
        title="Pizza",
    )

    query = f"""
    query {{
      recipe(slug: "{recipe.slug}") {{
        title
        slug
        category {{
          name
          slug
        }}
        author {{
          username
          email
        }}
      }}
    }}
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": query},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    recipe_data = data["data"]["recipe"]

    assert recipe_data["title"] == "Pizza"

    assert recipe_data["category"]["name"] == recipe.category.name
    assert recipe_data["category"]["slug"] == recipe.category.slug

    assert recipe_data["author"]["username"] == recipe.author.username
    assert recipe_data["author"]["email"] == recipe.author.email


@pytest.mark.django_db
def test_recipe_with_ingredients_query(graphql_client):
    recipe = RecipeFactory(title="Pizza")

    cheese = IngredientFactory(name="Cheese")
    tomato = IngredientFactory(name="Tomato")

    RecipeIngredientFactory(
        recipe=recipe,
        ingredient=cheese,
        amount=200,
    )

    RecipeIngredientFactory(
        recipe=recipe,
        ingredient=tomato,
        amount=150,
    )

    query = f"""
    query {{
      recipe(slug: "{recipe.slug}") {{
        title

        category {{
          name
        }}

        author {{
          username
        }}

        ingredients {{
          name
        }}
      }}
    }}
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": query},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    recipe_data = data["data"]["recipe"]

    assert recipe_data["title"] == "Pizza"

    assert recipe_data["category"]["name"] == recipe.category.name

    assert recipe_data["author"]["username"] == recipe.author.username

    ingredient_names = {ingredient["name"] for ingredient in recipe_data["ingredients"]}

    assert ingredient_names == {
        "Cheese",
        "Tomato",
    }


@pytest.mark.django_db
def test_recipe_with_all_related_objects_query(graphql_client):
    recipe = RecipeFactory(title="Pizza")

    cheese = IngredientFactory(name="Cheese")
    tomato = IngredientFactory(name="Tomato")

    RecipeIngredientFactory(
        recipe=recipe,
        ingredient=cheese,
        amount=200,
        unit=IngredientUnit.GRAM,
    )

    RecipeIngredientFactory(
        recipe=recipe,
        ingredient=tomato,
        amount=150,
        unit=IngredientUnit.GRAM,
    )

    StepFactory(
        recipe=recipe,
        order=1,
        instruction="Prepare dough",
    )

    StepFactory(
        recipe=recipe,
        order=2,
        instruction="Bake",
    )

    review = ReviewFactory(
        recipe=recipe,
        rating=5,
        comment="Excellent!",
    )

    FavoriteFactory(
        recipe=recipe,
        user=review.user,
    )

    query = f"""
    query {{
      recipe(slug: "{recipe.slug}") {{

        recipeIngredients {{
          amount
          unit
          ingredient {{
            name
          }}
        }}

        steps {{
          order
          instruction
        }}

        reviews {{
          rating
          comment
          user {{
            username
          }}
        }}

        favorites {{
          user {{
            username
          }}
        }}
      }}
    }}
    """

    response = graphql_client.post(
        "/graphql/",
        data={"query": query},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    recipe_data = data["data"]["recipe"]

    assert len(recipe_data["recipeIngredients"]) == 2
    assert len(recipe_data["steps"]) == 2
    assert len(recipe_data["reviews"]) == 1
    assert len(recipe_data["favorites"]) == 1

    ingredient_names = {
        item["ingredient"]["name"] for item in recipe_data["recipeIngredients"]
    }

    assert ingredient_names == {
        "Cheese",
        "Tomato",
    }

    assert recipe_data["steps"][0]["order"] == 1
    assert recipe_data["steps"][1]["order"] == 2

    assert recipe_data["reviews"][0]["rating"] == 5
    assert recipe_data["reviews"][0]["comment"] == "Excellent!"

    assert recipe_data["favorites"][0]["user"]["username"] == review.user.username
