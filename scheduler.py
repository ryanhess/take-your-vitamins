from dataclasses import dataclass
from backend import (
    IngredientAttributes,
    IngredientInPlanRequestResponse,
    SupplimentPlanResponse,
    ingredients,
)


@dataclass
class Ingredient:
    name: str
    attributes: IngredientAttributes


def apply_constraints_to_sups(
    request: list[IngredientInPlanRequestResponse],
) -> list[Ingredient]:
    ingredient_names_in_request = [ing.name for ing in request]
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


def bin_conflict_count(bin: set[Ingredient], take_not_with: set[str]) -> int:
    names_in_bin = {ing.name for ing in bin}
    num_conflicts = len(names_in_bin & take_not_with)
    return num_conflicts


def bin_suppliments_by_constraints(ings: list[Ingredient]) -> list[set[Ingredient]]:
    """
    We have by now made two problems out of this, before and after a meal. This function
    sorts into 3 bins: bin 0 is breakfast, bin 1 is lunch, bin 2 is dinner.
    """
    bins: list[set[Ingredient]] = [set(), set(), set()]

    # fmt: off
    sorted_ings = sorted(
        ings,
        key=lambda sup: 
            len(sup.attributes.take_not_with),
        reverse=True
    )
    # fmt: on

    for ing in sorted_ings:
        take_not_with = set(ing.attributes.take_not_with)
        conflict_counts = []

        for bin in bins:
            conflict_counts.append(bin_conflict_count(bin, take_not_with))

        fewest_conflicts = min(conflict_counts)
        target_index = conflict_counts.index(fewest_conflicts)

        bins[target_index].add(ing)

    return bins


def get_response_ingredients_from_bin(
    bin: set[Ingredient],
) -> list[IngredientInPlanRequestResponse]:
    ingredients_result = [IngredientInPlanRequestResponse(name=sup.name) for sup in bin]
    return ingredients_result


def transform_to_response(
    before_bins: list[set[Ingredient]], after_bins: list[set[Ingredient]]
) -> SupplimentPlanResponse:
    response = SupplimentPlanResponse(
        before_breakfast=get_response_ingredients_from_bin(before_bins[0]),
        before_lunch=get_response_ingredients_from_bin(before_bins[1]),
        before_dinner=get_response_ingredients_from_bin(before_bins[2]),
        after_breakfast=get_response_ingredients_from_bin(after_bins[0]),
        after_lunch=get_response_ingredients_from_bin(after_bins[1]),
        after_dinner=get_response_ingredients_from_bin(after_bins[2]),
    )
    return SupplimentPlanResponse()


def create_schedule(
    request: list[IngredientInPlanRequestResponse],
) -> SupplimentPlanResponse:
    request_sups_with_constraints = apply_constraints_to_sups(request)
    before_constrained_sups, after_constrained_sups = split_sups_before_after(
        request_sups_with_constraints
    )
    before_bins = bin_suppliments_by_constraints(before_constrained_sups)
    after_bins = bin_suppliments_by_constraints(after_constrained_sups)
    response = transform_to_response(before_bins=before_bins, after_bins=after_bins)
    return response
