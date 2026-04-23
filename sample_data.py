from enum import Enum

from models import IngredientAttributes, BeforeAfterFood


class Dataset(Enum):
    EMPTY = "empty"
    BASE = "base"
    EXERCISE = "exercise"
    FORCE_CONFLICT = "force_conflict"


DATASET = Dataset.EXERCISE


ingredient_datasets = {
    ### SET 0--empty set ###
    Dataset.EMPTY: {},
    ### SET 1--should produce exactly one in each category if I ask for all of these ###
    Dataset.BASE: {
        "Vitamin C": IngredientAttributes(
            take_not_with={"Vitamin B12", "Vitamin D"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Omega 3": IngredientAttributes(
            take_not_with={"Vitamin A", "Mugwort"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Vitamin B12": IngredientAttributes(
            take_not_with={"Vitamin C", "Vitamin D"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Vitamin A": IngredientAttributes(
            take_not_with={"Omega 3", "Mugwort"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Vitamin D": IngredientAttributes(
            take_not_with={"Vitamin C", "Vitamin B12"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Mugwort": IngredientAttributes(
            take_not_with={"Vitamin A", "Omega 3"},
            before_after_food=BeforeAfterFood("after"),
        ),
    },
    ### SET 2--Exercise the algorithm (generated)###
    Dataset.EXERCISE: {
        # --- Cluster 1: Classic vitamin conflicts (dense) ---
        "Vitamin C": IngredientAttributes(
            take_not_with={"Vitamin B12", "Copper", "Niacin"},
            before_after_food=BeforeAfterFood(
                "before",
            ),
        ),
        "Vitamin B12": IngredientAttributes(
            take_not_with={"Vitamin C", "Folate", "Vitamin B6"},
            before_after_food=BeforeAfterFood(
                "before",
            ),
        ),
        "Folate": IngredientAttributes(
            take_not_with={"Vitamin B12", "Green Tea Extract"},
            before_after_food=BeforeAfterFood(
                "before",
            ),
        ),
        "Vitamin B6": IngredientAttributes(
            take_not_with={"Vitamin B12", "Caffeine"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Niacin": IngredientAttributes(
            take_not_with={"Vitamin C", "Manganese"},
            before_after_food=BeforeAfterFood("before"),
        ),
        # --- Cluster 2: Fat-soluble vitamins competing for absorption ---
        "Vitamin D": IngredientAttributes(
            take_not_with={"Vitamin K2", "Vitamin A"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Vitamin A": IngredientAttributes(
            take_not_with={"Vitamin D", "Vitamin E", "Retinol"},
            before_after_food=BeforeAfterFood(
                "after",
            ),
        ),
        "Vitamin E": IngredientAttributes(
            take_not_with={"Vitamin A", "Vitamin K2", "Iron"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Vitamin K2": IngredientAttributes(
            take_not_with={"Vitamin D", "Vitamin E"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Retinol": IngredientAttributes(
            take_not_with={"Vitamin A", "Fish Oil"},
            before_after_food=BeforeAfterFood("after"),
        ),
        # --- Cluster 3: Mineral conflicts (chain pattern) ---
        "Calcium": IngredientAttributes(
            take_not_with={"Iron", "Magnesium", "Zinc"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Iron": IngredientAttributes(
            take_not_with={"Calcium", "Zinc", "Vitamin E", "Green Tea Extract"},
            before_after_food=BeforeAfterFood(
                "before",
            ),
        ),
        "Zinc": IngredientAttributes(
            take_not_with={"Calcium", "Iron", "Copper"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Magnesium": IngredientAttributes(
            take_not_with={"Calcium", "Manganese"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Copper": IngredientAttributes(
            take_not_with={"Zinc", "Vitamin C", "NAC"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Manganese": IngredientAttributes(
            take_not_with={"Magnesium", "Calcium"},
            before_after_food=BeforeAfterFood("before"),
        ),
        # --- Cluster 4: Herbal/extract conflicts ---
        "Green Tea Extract": IngredientAttributes(
            take_not_with={"Iron", "Folate", "Beta-Alanine"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Turmeric": IngredientAttributes(
            take_not_with={"Ashwagandha", "Quercetin"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Quercetin": IngredientAttributes(
            take_not_with={"Turmeric", "L-Theanine"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Ashwagandha": IngredientAttributes(
            take_not_with={"Turmeric", "L-Theanine"},
            before_after_food=BeforeAfterFood("after"),
        ),
        "Mugwort": IngredientAttributes(
            take_not_with={"Ashwagandha", "Fish Oil"},
            before_after_food=BeforeAfterFood("after"),
        ),
        # --- Cluster 5: Amino acids and performance supps ---
        "NAC": IngredientAttributes(
            take_not_with={"Copper", "Zinc"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "L-Theanine": IngredientAttributes(
            take_not_with={"Quercetin", "Ashwagandha"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Beta-Alanine": IngredientAttributes(
            take_not_with={"Green Tea Extract", "Taurine"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Taurine": IngredientAttributes(
            take_not_with={"Beta-Alanine"}, before_after_food=BeforeAfterFood("after")
        ),
        "Creatine": IngredientAttributes(
            take_not_with={"Caffeine"}, before_after_food=BeforeAfterFood("after")
        ),
        "Caffeine": IngredientAttributes(
            take_not_with={"Creatine", "Iron", "L-Theanine"},
            before_after_food=BeforeAfterFood("before"),
        ),
        # --- A few with no conflicts (easy to place) ---
        "Probiotics": IngredientAttributes(
            take_not_with=set(), before_after_food=BeforeAfterFood("before")
        ),
        "Collagen": IngredientAttributes(
            take_not_with=set(), before_after_food=BeforeAfterFood("after")
        ),
        "Fish Oil": IngredientAttributes(
            take_not_with={"Retinol"}, before_after_food=BeforeAfterFood("after")
        ),
    },
    ## Delibterately cause conflicts
    Dataset.FORCE_CONFLICT: {
        "Alpha": IngredientAttributes(
            take_not_with={"Bravo", "Charlie", "Delta"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Bravo": IngredientAttributes(
            take_not_with={"Alpha", "Charlie", "Delta"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Charlie": IngredientAttributes(
            take_not_with={"Alpha", "Bravo", "Delta"},
            before_after_food=BeforeAfterFood("before"),
        ),
        "Delta": IngredientAttributes(
            take_not_with={"Alpha", "Bravo", "Charlie"},
            before_after_food=BeforeAfterFood("before"),
        ),
    },
}


ingredients = ingredient_datasets[DATASET]
