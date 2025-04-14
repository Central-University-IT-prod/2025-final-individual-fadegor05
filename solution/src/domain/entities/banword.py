from dataclasses import dataclass

from src.domain.base import BaseDomain


@dataclass
class BanwordEntity(BaseDomain):
    word: str
