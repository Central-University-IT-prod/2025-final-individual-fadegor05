from src.domain.aggregates.click import ClickAggregate
from src.domain.repositories.event_repository import EventRepository


class ClickRepository(EventRepository[ClickAggregate]):
    pass
