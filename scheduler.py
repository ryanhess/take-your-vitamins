from dataclasses import dataclass
from backend import (
    IngredientAttributes,
    IngredientInPlanRequestResponse,
    SupplimentPlanResponse,
)


@dataclass
class Ingredient:
    name: str
    attributes: IngredientAttributes


def apply_constraints_to_sups(
    request: list[IngredientInPlanRequestResponse],
) -> list[Ingredient]:
    return []


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


def bin_suppliments_by_constraints(sups: list[Ingredient]) -> list[list[Ingredient]]:
    return []


def get_response_ingredients_from_bin(
    bin: list[Ingredient],
) -> list[IngredientInPlanRequestResponse]:
    ingredients_result = [IngredientInPlanRequestResponse(name=sup.name) for sup in bin]
    return ingredients_result


def transform_to_response(
    before_bins: list[list[Ingredient]], after_bins: list[list[Ingredient]]
) -> SupplimentPlanResponse:
    response = SupplimentPlanResponse(
        before_breakfast=get_response_ingredients_from_bin(before_bins[0]),
        before_lunch=get_response_ingredients_from_bin(before_bins[1]),
        before_dinner=get_response_ingredients_from_bin(before_bins[2]),
        after_breakfast=get_response_ingredients_from_bin(after_bins[0]),
        after_lunch=get_response_ingredients_from_bin(after_bins[1]),
        after_dinner=get_response_ingredients_from_bin(after_bins[0]),
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
