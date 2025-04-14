from dataclasses import dataclass

from src.domain.base import BaseDomain


@dataclass
class AdvertiserEntity(BaseDomain):
    telegram_id: int | None
    name: str
