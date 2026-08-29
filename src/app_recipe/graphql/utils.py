from django.db.models import Prefetch
from graphql import GraphQLError

from ..models import Category, Favorite, Ingredient, Recipe, Review, User


def get_recipe_by_slug(slug: str) -> Recipe:
    recipe = (
        Recipe.objects.select_related(
            "category",
            "author",
        )
        .prefetch_related(
            "ingredients",
            "steps",
            Prefetch(
                "reviews",
                queryset=Review.objects.select_related("user"),
            ),
            Prefetch(
                "favorites",
                queryset=Favorite.objects.select_related("user"),
            ),
        )
        .filter(
            slug=slug,
        )
        .first()
    )
    if recipe is None:
        raise GraphQLError(f"Recipe with slug '{slug}' was not found.")

    return recipe


def get_category_by_slug(slug: str) -> Category:
    category = Category.objects.filter(slug=slug).first()
    if category is None:
        raise GraphQLError(f"Category with slug '{slug}' was not found.")

    return category


def get_ingredient_by_name(name: str) -> Ingredient:
    ingredient = Ingredient.objects.filter(name=name).first()
    if ingredient is None:
        raise GraphQLError(f"Ingredient '{name}' was not found.")

    return ingredient


def get_user_by_username(username: str) -> User:
    user = User.objects.filter(username=username).first()
    if user is None:
        raise GraphQLError(f"User '{username}' was not found.")

    return user


def get_current_user(info):
    user = info.context.user
    if user.is_anonymous:
        raise GraphQLError("Authentication required.")

    return user


def get_review(recipe: Recipe, user: User) -> Review:
    review = (
        Review.objects.select_related(
            "recipe",
            "user",
        )
        .filter(
            recipe=recipe,
            user=user,
        )
        .first()
    )
    if review is None:
        raise GraphQLError("Review was not found.")

    return review


def validate_rating(rating: int) -> None:
    if not 1 <= rating <= 5:
        raise GraphQLError("Rating must be between 1 and 5.")


def get_favorite(recipe: Recipe, user: User) -> Favorite:
    favorite = (
        Favorite.objects.select_related(
            "recipe",
            "user",
        )
        .filter(
            recipe=recipe,
            user=user,
        )
        .first()
    )
    if favorite is None:
        raise GraphQLError("Favorite was not found.")

    return favorite


def check_recipe_owner(recipe: Recipe, user: User) -> None:
    if recipe.author != user:
        raise GraphQLError("You do not have permission to modify this recipe.")
