from src.domain.value_objects.targeting import Targeting
from src.presentation.rest.schemas.targeting_schema import ITargetRead


class TargetingMapper:
    @staticmethod
    def to_read_schema(domain: Targeting) -> ITargetRead:
        return ITargetRead(
            gender=domain.gender,
            age_from=domain.age_from,
            age_to=domain.age_to,
            location=domain.location,
        )

    @staticmethod
    def to_domain(schema: ITargetRead) -> Targeting:
        return Targeting(
            gender=schema.gender,
            age_from=schema.age_from,
            age_to=schema.age_to,
            location=schema.location,
        )
