from ..shikaku._seed_type import SeedType


class PatchSeedType(SeedType, total=False):
    area: int | None
    shape: str | None
