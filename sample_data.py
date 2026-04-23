from enum import Enum

from models import IngredientOrm


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
        "Vitamin C": IngredientOrm(
            take_not_with={"Vitamin B12", "Vitamin D"}, before_after_food="before"
        ),
        "Omega 3": IngredientOrm(
            take_not_with={"Vitamin A", "Mugwort"}, before_after_food="after"
        ),
        "Vitamin B12": IngredientOrm(
            take_not_with={"Vitamin C", "Vitamin D"}, before_after_food="before"
        ),
        "Vitamin A": IngredientOrm(
            take_not_with={"Omega 3", "Mugwort"}, before_after_food="after"
        ),
        "Vitamin D": IngredientOrm(
            take_not_with={"Vitamin C", "Vitamin B12"}, before_after_food="before"
        ),
        "Mugwort": IngredientOrm(
            take_not_with={"Vitamin A", "Omega 3"}, before_after_food="after"
        ),
    },
    ### SET 2--Exercise the algorithm (generated)###
    Dataset.EXERCISE: {
        # --- Cluster 1: Classic vitamin conflicts (dense) ---
        "Vitamin C": IngredientOrm(
            take_not_with={"Vitamin B12", "Copper", "Niacin"},
            before_after_food="before",
        ),
        "Vitamin B12": IngredientOrm(
            take_not_with={"Vitamin C", "Folate", "Vitamin B6"},
            before_after_food="before",
        ),
        "Folate": IngredientOrm(
            take_not_with={"Vitamin B12", "Green Tea Extract"},
            before_after_food="before",
        ),
        "Vitamin B6": IngredientOrm(
            take_not_with={"Vitamin B12", "Caffeine"}, before_after_food="before"
        ),
        "Niacin": IngredientOrm(
            take_not_with={"Vitamin C", "Manganese"}, before_after_food="before"
        ),
        # --- Cluster 2: Fat-soluble vitamins competing for absorption ---
        "Vitamin D": IngredientOrm(
            take_not_with={"Vitamin K2", "Vitamin A"}, before_after_food="after"
        ),
        "Vitamin A": IngredientOrm(
            take_not_with={"Vitamin D", "Vitamin E", "Retinol"},
            before_after_food="after",
        ),
        "Vitamin E": IngredientOrm(
            take_not_with={"Vitamin A", "Vitamin K2", "Iron"}, before_after_food="after"
        ),
        "Vitamin K2": IngredientOrm(
            take_not_with={"Vitamin D", "Vitamin E"}, before_after_food="after"
        ),
        "Retinol": IngredientOrm(
            take_not_with={"Vitamin A", "Fish Oil"}, before_after_food="after"
        ),
        # --- Cluster 3: Mineral conflicts (chain pattern) ---
        "Calcium": IngredientOrm(
            take_not_with={"Iron", "Magnesium", "Zinc"}, before_after_food="after"
        ),
        "Iron": IngredientOrm(
            take_not_with={"Calcium", "Zinc", "Vitamin E", "Green Tea Extract"},
            before_after_food="before",
        ),
        "Zinc": IngredientOrm(
            take_not_with={"Calcium", "Iron", "Copper"}, before_after_food="before"
        ),
        "Magnesium": IngredientOrm(
            take_not_with={"Calcium", "Manganese"}, before_after_food="after"
        ),
        "Copper": IngredientOrm(
            take_not_with={"Zinc", "Vitamin C", "NAC"}, before_after_food="before"
        ),
        "Manganese": IngredientOrm(
            take_not_with={"Magnesium", "Calcium"}, before_after_food="before"
        ),
        # --- Cluster 4: Herbal/extract conflicts ---
        "Green Tea Extract": IngredientOrm(
            take_not_with={"Iron", "Folate", "Beta-Alanine"}, before_after_food="before"
        ),
        "Turmeric": IngredientOrm(
            take_not_with={"Ashwagandha", "Quercetin"}, before_after_food="after"
        ),
        "Quercetin": IngredientOrm(
            take_not_with={"Turmeric", "L-Theanine"}, before_after_food="before"
        ),
        "Ashwagandha": IngredientOrm(
            take_not_with={"Turmeric", "L-Theanine"}, before_after_food="after"
        ),
        "Mugwort": IngredientOrm(
            take_not_with={"Ashwagandha", "Fish Oil"}, before_after_food="after"
        ),
        # --- Cluster 5: Amino acids and performance supps ---
        "NAC": IngredientOrm(
            take_not_with={"Copper", "Zinc"}, before_after_food="before"
        ),
        "L-Theanine": IngredientOrm(
            take_not_with={"Quercetin", "Ashwagandha"}, before_after_food="before"
        ),
        "Beta-Alanine": IngredientOrm(
            take_not_with={"Green Tea Extract", "Taurine"}, before_after_food="before"
        ),
        "Taurine": IngredientOrm(
            take_not_with={"Beta-Alanine"}, before_after_food="after"
        ),
        "Creatine": IngredientOrm(
            take_not_with={"Caffeine"}, before_after_food="after"
        ),
        "Caffeine": IngredientOrm(
            take_not_with={"Creatine", "Iron", "L-Theanine"}, before_after_food="before"
        ),
        # --- A few with no conflicts (easy to place) ---
        "Probiotics": IngredientOrm(take_not_with=set(), before_after_food="before"),
        "Collagen": IngredientOrm(take_not_with=set(), before_after_food="after"),
        "Fish Oil": IngredientOrm(take_not_with={"Retinol"}, before_after_food="after"),
    },
    ## Delibterately cause conflicts
    Dataset.FORCE_CONFLICT: {
        "Alpha": IngredientOrm(
            take_not_with={"Bravo", "Charlie", "Delta"}, before_after_food="before"
        ),
        "Bravo": IngredientOrm(
            take_not_with={"Alpha", "Charlie", "Delta"}, before_after_food="before"
        ),
        "Charlie": IngredientOrm(
            take_not_with={"Alpha", "Bravo", "Delta"}, before_after_food="before"
        ),
        "Delta": IngredientOrm(
            take_not_with={"Alpha", "Bravo", "Charlie"}, before_after_food="before"
        ),
    },
}


ingredients = ingredient_datasets[DATASET]
