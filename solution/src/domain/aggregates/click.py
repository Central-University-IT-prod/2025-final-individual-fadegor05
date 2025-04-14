from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.base import BaseDomain


@dataclass
class ClickAggregate(BaseDomain):
    client_id: UUID
    campaign_id: UUID
    cost: Decimal
    date: int
