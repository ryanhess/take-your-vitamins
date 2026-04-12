from dataclasses import dataclass
from models import (
    IngredientAttributes,
    IngredientInRequest,
    IngredientInResponse,
    TimeSlots,
    SupplimentPlanResponse,
)
from sample_data import ingredients


@dataclass
class Ingredient:
    name: str
    attributes: IngredientAttributes
    DEV_conflict_count: int = 0

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        is_instance = isinstance(other, Ingredient)
        return is_instance and self.name == other.name


type Bin = set[Ingredient]
type BinList = list[Bin]


def apply_constraints_to_sups(
    request: list[IngredientInRequest],
) -> list[Ingredient]:
    ingredient_names_in_request = [ingred.name for ingred in request]
    ingredient_objects_from_request = []

    for name in ingredient_names_in_request:
        # intentionally allow a key error to raise if name isnt in ingredients. For now.
        attributes_from_database = ingredients[name]
        database_take_not_with = attributes_from_database.take_not_with

        narrowed_take_not_with = list(
            set(database_take_not_with).intersection(ingredient_names_in_request)
        )

        new_attributes = IngredientAttributes(
            take_not_with=narrowed_take_not_with,
            before_after_food=attributes_from_database.before_after_food,
        )

        new_ingredient_object = Ingredient(name=name, attributes=new_attributes)
        ingredient_objects_from_request.append(new_ingredient_object)

    return ingredient_objects_from_request


def split_sups_before_after(
    sups: list[Ingredient],
) -> tuple[list[Ingredient], list[Ingredient]]:
    before = []
    after = []
    for sup in sups:
        if sup.attributes.before_after_food == "before":
            before.append(sup)
        else:
            after.append(sup)
    return (before, after)


def bin_conflict_count(bin: Bin, take_not_with: set[str]) -> int:
    names_in_bin = {ingred.name for ingred in bin}
    num_conflicts = len(names_in_bin & take_not_with)
    return num_conflicts


def bin_suppliments_by_constraints(ingreds: list[Ingredient]) -> BinList:
    """
    bins[0] is breakfast, bins[1] is lunch, bins[2] is dinner.
    """
    bins: BinList = [set(), set(), set()]

    # fmt: off
    sorted_ingreds = sorted(
        ingreds,
        key=lambda sup: 
            len(sup.attributes.take_not_with),
        reverse=True
    )
    # fmt: on

    for ingred in sorted_ingreds:
        take_not_with = set(ingred.attributes.take_not_with)
        conflict_counts = []

        for bin in bins:
            conflict_counts.append(bin_conflict_count(bin, take_not_with))

        fewest_conflicts = min(conflict_counts)
        target_index = conflict_counts.index(fewest_conflicts)

        ingred.DEV_conflict_count = fewest_conflicts
        bins[target_index].add(ingred)

    return bins


def get_response_ingredients_from_bin(
    bin: Bin,
) -> list[IngredientInResponse]:
    # fmt: off
    ingredients_result = [
        IngredientInResponse(
            name=sup.name,
            DEV__conflict_count=sup.DEV_conflict_count
        ) for sup in bin
    ]
    # fmt: on
    return ingredients_result


def get_total_conflict_count(before: BinList, after: BinList) -> int:
    total_count = 0
    all_bins: BinList = before + after

    for bin in all_bins:
        total_count += sum(ingred.DEV_conflict_count for ingred in bin)

    return total_count


def transform_to_response(
    before_bins: BinList, after_bins: BinList
) -> SupplimentPlanResponse:
    response = SupplimentPlanResponse(
        DEV_total_conflict_count=get_total_conflict_count(before_bins, after_bins),
        schedule=TimeSlots(
            before_breakfast=get_response_ingredients_from_bin(before_bins[0]),
            before_lunch=get_response_ingredients_from_bin(before_bins[1]),
            before_dinner=get_response_ingredients_from_bin(before_bins[2]),
            after_breakfast=get_response_ingredients_from_bin(after_bins[0]),
            after_lunch=get_response_ingredients_from_bin(after_bins[1]),
            after_dinner=get_response_ingredients_from_bin(after_bins[2]),
        ),
    )
    return response


def create_schedule(
    request: list[IngredientInRequest],
) -> SupplimentPlanResponse:
    request_sups_with_constraints = apply_constraints_to_sups(request)
    before_constrained_sups, after_constrained_sups = split_sups_before_after(
        request_sups_with_constraints
    )
    before_bins = bin_suppliments_by_constraints(before_constrained_sups)
    after_bins = bin_suppliments_by_constraints(after_constrained_sups)
    response = transform_to_response(before_bins=before_bins, after_bins=after_bins)
    return response
