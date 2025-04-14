from dataclasses import dataclass

from src.core.enums import GenderEnum
from src.domain.base import BaseDomain


@dataclass
class ClientEntity(BaseDomain):
    login: str
    age: int
    location: str
    gender: GenderEnum
