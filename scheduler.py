from dataclasses import dataclass
from models import (
    IngredientInRequest,
    IngredientResponse,
    IngredientResponse,
    IngredientOrm,
    TimeSlots,
    SupplementPlanResponse,
)
from numpy import array, array_split, where
from numpy.random import choice
from string import ascii_lowercase as ascii
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


DISTRIBUTE_SLOTS = True


type Bin = list[IngredientResponse]
type BinList = list[Bin]


async def get_relevant_ingred_obj_from_valid_name(
    request_names: list[str], ing_orm: IngredientOrm
) -> IngredientResponse:
    take_not_with_ingredients = await ing_orm.take_not_with()
    take_not_with_names = {ingred.name for ingred in take_not_with_ingredients}

    narrowed_take_not_with_names = take_not_with_names.intersection(request_names)

    ingredient_response_dict = {
        attr: getattr(ing_orm, attr) for attr in ["name", "before_after_food"]
    }
    ingredient_response_dict["take_not_with"] = narrowed_take_not_with_names

    ingredient_object_with_relevant_attr = IngredientResponse(
        **ingredient_response_dict
    )
    return ingredient_object_with_relevant_attr


async def apply_constraints_to_sups(
    request: list[IngredientInRequest], db_conn: AsyncSession
) -> tuple[list[IngredientResponse], list[str]]:
    ingred_names_in_request = [ingred.name for ingred in request]
    ingred_objects_from_request = []
    names_not_found = []

    for name in ingred_names_in_request:
        result = await db_conn.execute(
            select(IngredientOrm).where(IngredientOrm.name == name)
        )
        ingred_in_db = result.scalars().one_or_none()

        if ingred_in_db is None:
            print(f"{name} not found in database.")
            names_not_found.append(name)
        else:
            relevant_ingred_obj = await get_relevant_ingred_obj_from_valid_name(
                request_names=ingred_names_in_request,
                ing_orm=ingred_in_db,
            )
            ingred_objects_from_request.append(relevant_ingred_obj)

    return ingred_objects_from_request, names_not_found


def split_sups_before_after(
    sups: list[IngredientResponse],
) -> tuple[list[IngredientResponse], list[IngredientResponse]]:
    before = []
    after = []
    for sup in sups:
        if sup.before_after_food == "before":
            before.append(sup)
        else:
            after.append(sup)
    return (before, after)


def bin_conflict_count(bin: Bin, take_not_with: set[str]) -> int:
    names_in_bin = {ingred.name for ingred in bin}
    num_conflicts = len(names_in_bin & take_not_with)
    return num_conflicts


def get_best_bins(counts: list[int], target_count: int) -> list[int]:
    counts_arr = array(counts)
    (best_bins,) = where(counts_arr == target_count)
    return list(best_bins)


def select_best_bin_by_ingred_name(
    counts: list[int], min_conflict_count: int, name: str
) -> int:
    best_bins = get_best_bins(counts, min_conflict_count)
    number_of_best_bins = len(best_bins)
    letter_index_groups = array_split(range(26), number_of_best_bins)
    first_char_lowercase = name[0].lower()
    first_char_letter_index = ord(first_char_lowercase) - ord("a")

    the_bin = None
    for i, group in enumerate(letter_index_groups):
        if first_char_letter_index in group:
            the_bin = best_bins[i]
            break

    if the_bin is None:
        the_bin = best_bins[-1]

    return the_bin


def bin_supplements_by_constraints(ingreds: list[IngredientResponse]) -> BinList:
    """
    bins[0] is breakfast, bins[1] is lunch, bins[2] is dinner.
    """
    bins: BinList = [[], [], []]

    # fmt: off
    sorted_ingreds = sorted(
        ingreds,
        key=lambda sup: 
            len(sup.take_not_with),
        reverse=True
    )
    # fmt: on

    for ingred in sorted_ingreds:
        take_not_with = set(ingred.take_not_with)
        conflict_counts = []

        for bin in bins:
            conflict_counts.append(bin_conflict_count(bin, take_not_with))

        min_conflicts = min(conflict_counts)

        if DISTRIBUTE_SLOTS:
            # fmt: off
            target_index = select_best_bin_by_ingred_name(
                counts=conflict_counts,
                min_conflict_count=min_conflicts,
                name=ingred.name
            )
            # fmt: on
        else:
            # just groups the answers towards the morning.
            target_index = conflict_counts.index(min_conflicts)

        ingred.DEV_conflict_count = min_conflicts
        bins[target_index].append(ingred)

    return bins


def get_total_conflict_count(before: BinList, after: BinList) -> int:
    total_count = 0
    all_bins: BinList = before + after

    for bin in all_bins:
        total_count += sum(ingred.DEV_conflict_count for ingred in bin)

    return total_count


def transform_to_response(before: BinList, after: BinList) -> SupplementPlanResponse:
    response = SupplementPlanResponse(
        DEV_total_conflict_count=get_total_conflict_count(before, after),
        schedule=TimeSlots(
            before_breakfast=before[0],
            before_lunch=before[1],
            before_dinner=before[2],
            after_breakfast=after[0],
            after_lunch=after[1],
            after_dinner=after[2],
        ),
    )
    return response


async def create_schedule(
    request: list[IngredientInRequest], db_conn: AsyncSession
) -> SupplementPlanResponse:
    (request_sups_with_constraints, names_not_in_db) = await apply_constraints_to_sups(
        request, db_conn
    )
    before_constrained_sups, after_constrained_sups = split_sups_before_after(
        request_sups_with_constraints
    )
    before_bins = bin_supplements_by_constraints(before_constrained_sups)
    after_bins = bin_supplements_by_constraints(after_constrained_sups)
    response = transform_to_response(before=before_bins, after=after_bins)
    response.supplements_not_found = names_not_in_db
    return response
