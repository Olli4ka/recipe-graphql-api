import pytest

from ..models import Favorite, Recipe, Review
from .factories import (
    CategoryFactory,
    FavoriteFactory,
    RecipeFactory,
    ReviewFactory
)


# ==========================================================
# Recipe
# ==========================================================
@pytest.mark.django_db
def test_create_recipe_mutation(authenticated_graphql_client):
    category = CategoryFactory(
        name="Pizza",
        slug="pizza",
    )

    mutation = """
    mutation CreateRecipe($input: RecipeInput!) {
      createRecipe(input: $input) {
        recipe {
          title
          slug
          cookingTime
          category {
            slug
          }
        }
      }
    }
    """

    variables = {
        "input": {
            "title": "Carbonara",
            "description": "Italian pasta",
            "cookingTime": 25,
            "categorySlug": "pizza",
        }
    }

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={
            "query": mutation,
            "variables": variables,
        },
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    recipe = data["data"]["createRecipe"]["recipe"]

    assert recipe["title"] == "Carbonara"
    assert recipe["cookingTime"] == 25
    assert recipe["category"]["slug"] == "pizza"

    assert Recipe.objects.filter(title="Carbonara").exists()


@pytest.mark.django_db
def test_update_recipe_mutation(
    authenticated_graphql_client,
    user,
):
    category = CategoryFactory(
        name="Pizza",
        slug="pizza",
    )

    RecipeFactory(
        title="Carbonara",
        slug="carbonara",
        category=category,
        author=user,
    )

    mutation = """
    mutation {
      updateRecipe(
        input:{
          slug:"carbonara"
          title:"New Carbonara"
        }
      ){
        recipe{
          title
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    recipe = data["data"]["updateRecipe"]["recipe"]

    assert recipe["title"] == "New Carbonara"

    assert Recipe.objects.get(slug="carbonara").title == "New Carbonara"


@pytest.mark.django_db
def test_update_recipe_by_non_owner(
    authenticated_client,
    owner,
    intruder,
):
    category = CategoryFactory(
        name="Pizza",
        slug="pizza",
    )

    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
        category=category,
        author=owner,
    )

    client = authenticated_client(intruder)

    mutation = """
    mutation {
      updateRecipe(
        input:{
          slug:"carbonara"
          title:"Hacked Recipe"
        }
      ){
        recipe{
          title
        }
      }
    }
    """

    response = client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert "errors" in data

    recipe.refresh_from_db()

    assert recipe.title == "Carbonara"


@pytest.mark.django_db
def test_delete_recipe_by_non_owner(
    authenticated_client,
    owner,
    intruder,
):
    category = CategoryFactory(
        name="Pizza",
        slug="pizza",
    )

    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
        category=category,
        author=owner,
    )

    client = authenticated_client(intruder)

    mutation = """
    mutation {
      deleteRecipe(
        slug: "carbonara"
      ) {
        success
        message
      }
    }
    """

    response = client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert "errors" in data

    assert Recipe.objects.filter(slug="carbonara").exists()


# ==========================================================
# Review
# ==========================================================
@pytest.mark.django_db
def test_create_review_mutation(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    mutation = """
    mutation {
      createReview(
        input: {
          recipeSlug: "carbonara"
          rating: 5
          comment: "Absolutely delicious!"
        }
      ) {
        review {
          rating
          comment
          recipe {
            slug
          }
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    review = data["data"]["createReview"]["review"]

    assert review["rating"] == 5
    assert review["comment"] == "Absolutely delicious!"
    assert review["recipe"]["slug"] == "carbonara"

    assert Review.objects.filter(
        recipe=recipe,
        user=user,
    ).exists()


@pytest.mark.django_db
def test_create_review_twice_by_same_user(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    ReviewFactory(
        recipe=recipe,
        user=user,
        rating=5,
        comment="First review",
    )

    mutation = """
    mutation {
      createReview(
        input: {
          recipeSlug: "carbonara"
          rating: 4
          comment: "Second review"
        }
      ) {
        review {
          rating
          comment
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("You have already reviewed this recipe.")

    assert (
        Review.objects.filter(
            recipe=recipe,
            user=user,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_create_review_with_invalid_low_rating(
    authenticated_graphql_client,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    mutation = """
    mutation {
      createReview(
        input: {
          recipeSlug: "carbonara"
          rating: 0
          comment: "Bad rating"
        }
      ) {
        review {
          rating
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("Rating must be between 1 and 5.")

    assert not Review.objects.filter(
        recipe=recipe,
    ).exists()


@pytest.mark.django_db
def test_create_review_with_invalid_high_rating(
    authenticated_graphql_client,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    mutation = """
    mutation {
      createReview(
        input: {
          recipeSlug: "carbonara"
          rating: 6
          comment: "Too good"
        }
      ) {
        review {
          rating
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("Rating must be between 1 and 5.")

    assert not Review.objects.filter(
        recipe=recipe,
    ).exists()


@pytest.mark.django_db
def test_update_review_mutation(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    ReviewFactory(
        recipe=recipe,
        user=user,
        rating=3,
        comment="It was okay.",
    )

    mutation = """
    mutation {
      updateReview(
        input: {
          recipeSlug: "carbonara"
          rating: 5
          comment: "Absolutely delicious!"
        }
      ) {
        review {
          rating
          comment
          recipe {
            slug
          }
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    review = data["data"]["updateReview"]["review"]

    assert review["rating"] == 5
    assert review["comment"] == "Absolutely delicious!"
    assert review["recipe"]["slug"] == "carbonara"

    updated_review = Review.objects.get(
        recipe=recipe,
        user=user,
    )

    assert updated_review.rating == 5
    assert updated_review.comment == "Absolutely delicious!"


@pytest.mark.django_db
def test_update_review_by_non_owner(
    authenticated_client,
    owner,
    intruder,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
        author=owner,
    )

    ReviewFactory(
        recipe=recipe,
        user=owner,
        rating=3,
        comment="It was okay.",
    )

    client = authenticated_client(intruder)

    mutation = """
    mutation {
      updateReview(
        input: {
          recipeSlug: "carbonara"
          rating: 5
          comment: "Hacked review"
        }
      ) {
        review {
          rating
          comment
        }
      }
    }
    """

    response = client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("Review was not found.")

    review = Review.objects.get(
        recipe=recipe,
        user=owner,
    )

    assert review.rating == 3
    assert review.comment == "It was okay."


@pytest.mark.django_db
def test_delete_review_mutation(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    review = ReviewFactory(
        recipe=recipe,
        user=user,
        rating=5,
        comment="Absolutely delicious!",
    )

    mutation = """
    mutation {
      deleteReview(
        input: {
          recipeSlug: "carbonara"
        }
      ) {
        success
        message
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    result = data["data"]["deleteReview"]

    assert result["success"] is True
    assert result["message"] == "Review was deleted."

    assert not Review.objects.filter(
        pk=review.pk,
    ).exists()


@pytest.mark.django_db
def test_delete_review_by_non_owner(
    authenticated_client,
    owner,
    intruder,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
        author=owner,
    )

    review = ReviewFactory(
        recipe=recipe,
        user=owner,
        rating=5,
        comment="Absolutely delicious!",
    )

    client = authenticated_client(intruder)

    mutation = """
    mutation {
      deleteReview(
        input: {
          recipeSlug: "carbonara"
        }
      ) {
        success
        message
      }
    }
    """

    response = client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("Review was not found.")

    assert Review.objects.filter(
        pk=review.pk,
    ).exists()


# ==========================================================
# Favorite
# ==========================================================
@pytest.mark.django_db
def test_create_favorite_mutation(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    mutation = """
    mutation {
      createFavorite(
        input: {
          recipeSlug: "carbonara"
        }
      ) {
        favorite {
          recipe {
            slug
          }
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    favorite = data["data"]["createFavorite"]["favorite"]

    assert favorite["recipe"]["slug"] == "carbonara"

    assert Favorite.objects.filter(
        recipe=recipe,
        user=user,
    ).exists()


@pytest.mark.django_db
def test_create_favorite_twice_by_same_user(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    FavoriteFactory(
        recipe=recipe,
        user=user,
    )

    mutation = """
    mutation {
      createFavorite(
        input: {
          recipeSlug: "carbonara"
        }
      ) {
        favorite {
          recipe {
            slug
          }
        }
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("Recipe is already in favorites.")

    assert (
        Favorite.objects.filter(
            recipe=recipe,
            user=user,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_delete_favorite_mutation(
    authenticated_graphql_client,
    user,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
    )

    favorite = FavoriteFactory(
        recipe=recipe,
        user=user,
    )

    mutation = """
    mutation {
      deleteFavorite(
        input: {
          recipeSlug: "carbonara"
        }
      ) {
        success
        message
      }
    }
    """

    response = authenticated_graphql_client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" not in data

    result = data["data"]["deleteFavorite"]

    assert result["success"] is True
    assert result["message"] == ("Recipe was removed from favorites.")

    assert not Favorite.objects.filter(
        pk=favorite.pk,
    ).exists()


@pytest.mark.django_db
def test_delete_favorite_by_non_owner(
    authenticated_client,
    owner,
    intruder,
):
    recipe = RecipeFactory(
        title="Carbonara",
        slug="carbonara",
        author=owner,
    )

    favorite = FavoriteFactory(
        recipe=recipe,
        user=owner,
    )

    client = authenticated_client(intruder)

    mutation = """
    mutation {
      deleteFavorite(
        input: {
          recipeSlug: "carbonara"
        }
      ) {
        success
        message
      }
    }
    """

    response = client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json",
    )

    data = response.json()

    assert response.status_code == 200
    assert "errors" in data

    assert data["errors"][0]["message"] == ("Favorite was not found.")

    assert Favorite.objects.filter(
        pk=favorite.pk,
    ).exists()