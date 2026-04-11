from dataclasses import dataclass
from backend import (
    IngredientAttributes,
    IngredientInPlanRequest,
    SupplimentPlanResponse,
)


@dataclass
class Ingredient:
    name: str
    attributes: IngredientAttributes


def apply_constraints_to_sups(
    request: list[IngredientInPlanRequest],
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


def transform_to_response(
    before: list[list[Ingredient]], after: list[list[Ingredient]]
) -> SupplimentPlanResponse:
    return SupplimentPlanResponse()


def create_schedule(request: list[IngredientInPlanRequest]) -> SupplimentPlanResponse:
    request_sups_with_constraints = apply_constraints_to_sups(request)
    before_constrained_sups, after_constrained_sups = split_sups_before_after(
        request_sups_with_constraints
    )
    before_bins = bin_suppliments_by_constraints(before_constrained_sups)
    after_bins = bin_suppliments_by_constraints(after_constrained_sups)
    response = transform_to_response(before=before_bins, after=after_bins)
    return response
