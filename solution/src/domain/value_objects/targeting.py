from dataclasses import dataclass

from src.core.enums import AllGenderEnum


@dataclass
class Targeting:
    gender: AllGenderEnum | None = None
    age_from: int | None = None
    age_to: int | None = None
    location: str | None = None
