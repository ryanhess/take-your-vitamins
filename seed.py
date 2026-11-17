import asyncio
from enum import Enum

from sqlalchemy import select, func
from database import async_session
from models import OrmBase, IngredientOrm, IngredientConflicts, BeforeAfterFood, IngredientInSchedule, SupplementSchedule, TimeSlotNames


class Dataset(Enum):
    EMPTY = "empty"
    BASE = "base"
    EXERCISE = "exercise"
    FORCE_CONFLICT = "force_conflict"


DATASET = Dataset.EXERCISE


ingredient_datasets = {
    Dataset.EMPTY: {},
    Dataset.BASE: {
        "Vitamin C": BeforeAfterFood.before,
        "Omega 3": BeforeAfterFood.after,
        "Vitamin B12": BeforeAfterFood.before,
        "Vitamin A": BeforeAfterFood.after,
        "Vitamin D": BeforeAfterFood.before,
        "Mugwort": BeforeAfterFood.after,
    },
    Dataset.EXERCISE: {
        # --- Cluster 1: Classic vitamin conflicts (dense) ---
        "Vitamin C": BeforeAfterFood.before,
        "Vitamin B12": BeforeAfterFood.before,
        "Folate": BeforeAfterFood.before,
        "Vitamin B6": BeforeAfterFood.before,
        "Niacin": BeforeAfterFood.before,
        # --- Cluster 2: Fat-soluble vitamins competing for absorption ---
        "Vitamin D": BeforeAfterFood.after,
        "Vitamin A": BeforeAfterFood.after,
        "Vitamin E": BeforeAfterFood.after,
        "Vitamin K2": BeforeAfterFood.after,
        "Retinol": BeforeAfterFood.after,
        # --- Cluster 3: Mineral conflicts (chain pattern) ---
        "Calcium": BeforeAfterFood.after,
        "Iron": BeforeAfterFood.before,
        "Zinc": BeforeAfterFood.before,
        "Magnesium": BeforeAfterFood.after,
        "Copper": BeforeAfterFood.before,
        "Manganese": BeforeAfterFood.before,
        # --- Cluster 4: Herbal/extract conflicts ---
        "Green Tea Extract": BeforeAfterFood.before,
        "Turmeric": BeforeAfterFood.after,
        "Quercetin": BeforeAfterFood.before,
        "Ashwagandha": BeforeAfterFood.after,
        "Mugwort": BeforeAfterFood.after,
        # --- Cluster 5: Amino acids and performance supps ---
        "NAC": BeforeAfterFood.before,
        "L-Theanine": BeforeAfterFood.before,
        "Beta-Alanine": BeforeAfterFood.before,
        "Taurine": BeforeAfterFood.after,
        "Creatine": BeforeAfterFood.after,
        "Caffeine": BeforeAfterFood.before,
        # --- No conflicts ---
        "Probiotics": BeforeAfterFood.before,
        "Collagen": BeforeAfterFood.after,
        "Fish Oil": BeforeAfterFood.after,
    },
    Dataset.FORCE_CONFLICT: {
        "Alpha": BeforeAfterFood.before,
        "Bravo": BeforeAfterFood.before,
        "Charlie": BeforeAfterFood.before,
        "Delta": BeforeAfterFood.before,
    },
}

conflict_datasets = {
    Dataset.EMPTY: [],
    Dataset.BASE: [
        ("Vitamin C", "Vitamin B12"),
        ("Vitamin C", "Vitamin D"),
        ("Omega 3", "Vitamin A"),
        ("Omega 3", "Mugwort"),
        ("Vitamin B12", "Vitamin D"),
        ("Vitamin A", "Mugwort"),
    ],
    Dataset.EXERCISE: [
        # Cluster 1: Classic vitamin conflicts
        ("Vitamin C", "Vitamin B12"),
        ("Vitamin C", "Copper"),
        ("Vitamin C", "Niacin"),
        ("Vitamin B12", "Folate"),
        ("Vitamin B12", "Vitamin B6"),
        ("Folate", "Green Tea Extract"),
        ("Vitamin B6", "Caffeine"),
        ("Niacin", "Manganese"),
        # Cluster 2: Fat-soluble vitamins
        ("Vitamin D", "Vitamin K2"),
        ("Vitamin D", "Vitamin A"),
        ("Vitamin A", "Vitamin E"),
        ("Vitamin A", "Retinol"),
        ("Vitamin E", "Vitamin K2"),
        ("Vitamin E", "Iron"),
        ("Retinol", "Fish Oil"),
        # Cluster 3: Mineral conflicts
        ("Calcium", "Iron"),
        ("Calcium", "Magnesium"),
        ("Calcium", "Zinc"),
        ("Iron", "Zinc"),
        ("Iron", "Green Tea Extract"),
        ("Zinc", "Copper"),
        ("Magnesium", "Manganese"),
        ("Copper", "NAC"),
        # Cluster 4: Herbal/extract conflicts
        ("Turmeric", "Ashwagandha"),
        ("Turmeric", "Quercetin"),
        ("Quercetin", "L-Theanine"),
        ("Ashwagandha", "L-Theanine"),
        ("Mugwort", "Ashwagandha"),
        ("Mugwort", "Fish Oil"),
        # Cluster 5: Amino acids and performance supps
        ("NAC", "Zinc"),
        ("Beta-Alanine", "Green Tea Extract"),
        ("Beta-Alanine", "Taurine"),
        ("Creatine", "Caffeine"),
        ("Caffeine", "Iron"),
        ("Caffeine", "L-Theanine"),
    ],
    Dataset.FORCE_CONFLICT: [
        ("Alpha", "Bravo"),
        ("Alpha", "Charlie"),
        ("Alpha", "Delta"),
        ("Bravo", "Charlie"),
        ("Bravo", "Delta"),
        ("Charlie", "Delta"),
    ],
}


async def seed():
    ingredients = ingredient_datasets[DATASET]
    conflicts = conflict_datasets[DATASET]

    async with async_session() as session:
        for table in OrmBase.metadata.sorted_tables:
            count = (
                await session.execute(select(func.count()).select_from(table))
            ).scalar_one()
            if count > 0:
                print(f"Table '{table.name}' has {count} rows. Aborting seed.")
                return

        for name, before_after in ingredients.items():
            session.add(IngredientOrm(name=name, before_after_food=before_after))
        await session.flush()

        result = await session.execute(select(IngredientOrm))
        name_to_id = {row.name: row.id for row in result.scalars().all()}

        for name_a, name_b in conflicts:
            id_a = name_to_id[name_a]
            id_b = name_to_id[name_b]
            low, high = sorted([id_a, id_b])
            session.add(IngredientConflicts(id_a=low, id_b=high))

        schedule = SupplementSchedule(user_id=1)
        session.add(schedule)
        await session.flush()

        schedule_entries = [
            ("Vitamin C",       TimeSlotNames.before_breakfast),
            ("Vitamin B12",     TimeSlotNames.before_breakfast),
            ("Probiotics",      TimeSlotNames.before_breakfast),
            ("Vitamin D",       TimeSlotNames.after_breakfast),
            ("Vitamin A",       TimeSlotNames.after_breakfast),
            ("Magnesium",       TimeSlotNames.after_lunch),
            ("Turmeric",        TimeSlotNames.after_lunch),
            ("Zinc",            TimeSlotNames.before_dinner),
            ("Fish Oil",        TimeSlotNames.after_dinner),
            ("Ashwagandha",     TimeSlotNames.after_dinner),
        ]

        for name, slot in schedule_entries:
            session.add(IngredientInSchedule(
                ingredient_id=name_to_id[name],
                schedule_id=schedule.id,
                slot=slot,
            ))

        await session.commit()

    print(f"Seeded {len(ingredients)} ingredients, {len(conflicts)} conflicts, and 1 schedule with {len(schedule_entries)} entries.")


if __name__ == "__main__":
    asyncio.run(seed())
