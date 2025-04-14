from src.domain.aggregates.impression import ImpressionAggregate
from src.domain.repositories.event_repository import EventRepository


class ImpressionRepository(EventRepository[ImpressionAggregate]):
    pass
