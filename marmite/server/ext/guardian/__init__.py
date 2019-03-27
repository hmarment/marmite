from enum import Enum

BASE_URL = "https://content.guardianapis.com/"


class Endpoints(Enum):
    ListRecipes = (
        "search?tag=tone/recipes&api-key={API_KEY}"
        "&page={page}&page-size={page_size}"
        "&order-by={order_by}&show-tags=all"
    )
    GetRecipe = "{RECIPE_ID}?api-key={API_KEY}&show-fields=all&show-tags=all"


from . import content
from . import models
