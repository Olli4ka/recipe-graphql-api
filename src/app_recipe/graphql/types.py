import graphene
from graphene_django import DjangoObjectType

from ..models import (
    Category,
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Review,
    Step,
    User,
)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeIngredientType(DjangoObjectType):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class StepType(DjangoObjectType):
    class Meta:
        model = Step
        fields = "__all__"


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = "__all__"


class FavoriteType(DjangoObjectType):
    class Meta:
        model = Favorite
        fields = "__all__"


class RecipeListType(graphene.ObjectType):
    total_count = graphene.Int()
    has_next_page = graphene.Boolean()
    items = graphene.List(RecipeType)
