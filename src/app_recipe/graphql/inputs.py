import graphene


class RecipeInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    cooking_time = graphene.Int(required=True)

    category_slug = graphene.String(required=True)


class UpdateRecipeInput(graphene.InputObjectType):
    slug = graphene.String(required=True)

    title = graphene.String()
    description = graphene.String()
    cooking_time = graphene.Int()

    category_slug = graphene.String()


class ReviewInput(graphene.InputObjectType):
    recipe_slug = graphene.String(required=True)
    rating = graphene.Int(required=True)
    comment = graphene.String(required=True)


class UpdateReviewInput(graphene.InputObjectType):
    recipe_slug = graphene.String(required=True)
    rating = graphene.Int()
    comment = graphene.String()


class DeleteReviewInput(graphene.InputObjectType):
    recipe_slug = graphene.String(required=True)


class FavoriteInput(graphene.InputObjectType):
    recipe_slug = graphene.String(required=True)
