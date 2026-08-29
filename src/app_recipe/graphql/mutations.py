import graphene
import graphql_jwt
from graphql import GraphQLError

from ..models import Favorite, Recipe, Review
from .inputs import (
    DeleteReviewInput,
    FavoriteInput,
    RecipeInput,
    ReviewInput,
    UpdateRecipeInput,
    UpdateReviewInput,
)
from .types import FavoriteType, RecipeType, ReviewType
from .utils import (
    check_recipe_owner,
    get_category_by_slug,
    get_current_user,
    get_favorite,
    get_recipe_by_slug,
    get_review,
    validate_rating,
)


class CreateRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        input = RecipeInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        category = get_category_by_slug(input.category_slug)
        author = get_current_user(info)
        recipe = Recipe.objects.create(
            title=input.title,
            description=input.description,
            cooking_time=input.cooking_time,
            category=category,
            author=author,
        )
        return cls(recipe=recipe)


class UpdateRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        input = UpdateRecipeInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        recipe = get_recipe_by_slug(input.slug)
        user = get_current_user(info)

        check_recipe_owner(recipe, user)

        if input.title is not None:
            recipe.title = input.title

        if input.description is not None:
            recipe.description = input.description

        if input.cooking_time is not None:
            recipe.cooking_time = input.cooking_time

        if input.category_slug is not None:
            recipe.category = get_category_by_slug(input.category_slug)

        recipe.save()

        return cls(recipe=recipe)


class DeleteRecipe(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        slug = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, slug):
        recipe = get_recipe_by_slug(slug)
        user = get_current_user(info)

        check_recipe_owner(recipe, user)

        deleted_slug = recipe.slug

        recipe.delete()

        return cls(
            success=True, message=f"Recipe with slug '{deleted_slug}' was deleted."
        )


class CreateReview(graphene.Mutation):
    review = graphene.Field(ReviewType)

    class Arguments:
        input = ReviewInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        recipe = get_recipe_by_slug(input.recipe_slug)
        user = get_current_user(info)

        if Review.objects.filter(
            recipe=recipe,
            user=user,
        ).exists():
            raise GraphQLError("You have already reviewed this recipe.")

        validate_rating(input.rating)

        review = Review.objects.create(
            recipe=recipe,
            user=user,
            rating=input.rating,
            comment=input.comment,
        )

        return cls(review=review)


class UpdateReview(graphene.Mutation):
    review = graphene.Field(ReviewType)

    class Arguments:
        input = UpdateReviewInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        recipe = get_recipe_by_slug(input.recipe_slug)
        user = get_current_user(info)
        review = get_review(recipe, user)

        if input.comment is not None:
            review.comment = input.comment

        if input.rating is not None:
            validate_rating(input.rating)
            review.rating = input.rating

        review.save()

        return cls(review=review)


class DeleteReview(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        input = DeleteReviewInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        recipe = get_recipe_by_slug(input.recipe_slug)
        user = get_current_user(info)
        review = get_review(recipe, user)

        review.delete()

        return cls(success=True, message="Review was deleted.")


class CreateFavorite(graphene.Mutation):
    favorite = graphene.Field(FavoriteType)

    class Arguments:
        input = FavoriteInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        recipe = get_recipe_by_slug(input.recipe_slug)
        user = get_current_user(info)
        favorite, created = Favorite.objects.get_or_create(
            recipe=recipe,
            user=user,
        )

        if not created:
            raise GraphQLError("Recipe is already in favorites.")

        return cls(favorite=favorite)


class DeleteFavorite(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        input = FavoriteInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        recipe = get_recipe_by_slug(input.recipe_slug)
        user = get_current_user(info)
        favorite = get_favorite(recipe, user)

        favorite.delete()

        return cls(success=True, message="Recipe was removed from favorites.")


class Mutation(graphene.ObjectType):
    # ---------- JWT ----------
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    # ---------- Recipe ----------
    create_recipe = CreateRecipe.Field()
    update_recipe = UpdateRecipe.Field()
    delete_recipe = DeleteRecipe.Field()

    # ---------- Review ----------
    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
    delete_review = DeleteReview.Field()

    # ---------- Favorite ----------
    create_favorite = CreateFavorite.Field()
    delete_favorite = DeleteFavorite.Field()
