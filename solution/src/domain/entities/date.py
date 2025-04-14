from dataclasses import dataclass

from src.domain.base import BaseDomain


@dataclass
class DateEntity(BaseDomain):
    date: int
