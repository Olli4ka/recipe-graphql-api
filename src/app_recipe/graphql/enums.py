import graphene


class RecipeOrderEnum(graphene.Enum):
    TITLE = "title"
    TITLE_DESC = "-title"

    COOKING_TIME = "cooking_time"
    COOKING_TIME_DESC = "-cooking_time"

    CREATED = "created_at"
    CREATED_DESC = "-created_at"
