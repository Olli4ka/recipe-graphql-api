import graphene
from django.db.models import Prefetch

from ..models import Category, Favorite, Ingredient, Recipe, Review, User
from .enums import RecipeOrderEnum
from .types import (CategoryType, IngredientType, RecipeListType, RecipeType,
                    UserType)
from .utils import (get_category_by_slug, get_ingredient_by_name,
                    get_recipe_by_slug, get_user_by_username)


class Query(graphene.ObjectType):

    recipes = graphene.Field(
        RecipeListType,
        category=graphene.String(),
        author=graphene.String(),
        search=graphene.String(),
        order_by=RecipeOrderEnum(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    recipe = graphene.Field(
        RecipeType,
        slug=graphene.String(required=True),
    )

    categories = graphene.List(CategoryType)
    category = graphene.Field(
        CategoryType,
        slug=graphene.String(required=True),
    )

    ingredients = graphene.List(IngredientType)
    ingredient = graphene.Field(
        IngredientType,
        name=graphene.String(required=True),
    )

    users = graphene.List(UserType)
    user = graphene.Field(
        UserType,
        username=graphene.String(required=True),
    )

    def resolve_recipes(
        root,
        info,
        category=None,
        author=None,
        search=None,
        order_by=None,
        limit=None,
        offset=None,
    ):
        queryset = Recipe.objects.select_related("category", "author").prefetch_related(
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
        if category:
            queryset = queryset.filter(category__slug=category)

        if author:
            queryset = queryset.filter(author__username=author)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if order_by:
            queryset = queryset.order_by(order_by.value)

        total = queryset.count()

        if offset is not None:
            queryset = queryset[offset:]

        if limit is not None:
            queryset = queryset[:limit]

        has_next_page = False

        if limit is not None:
            has_next_page = total > (offset or 0) + limit

        return RecipeListType(
            total_count=total,
            has_next_page=has_next_page,
            items=queryset,
        )

    def resolve_recipe(root, info, slug):
        return get_recipe_by_slug(slug)

    def resolve_categories(root, info):
        return Category.objects.all()

    def resolve_category(root, info, slug):
        return get_category_by_slug(slug)

    def resolve_ingredient(root, info, name):
        return get_ingredient_by_name(name)

    def resolve_ingredients(root, info):
        return Ingredient.objects.all()

    def resolve_users(root, info):
        return User.objects.all()

    def resolve_user(root, info, username):
        return get_user_by_username(username)
