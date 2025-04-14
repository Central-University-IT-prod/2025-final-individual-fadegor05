from dataclasses import dataclass
from uuid import UUID

from src.domain.base import BaseDomain


@dataclass
class MLScoreAggregate(BaseDomain):
    client_id: UUID
    advertiser_id: UUID
    score: int
