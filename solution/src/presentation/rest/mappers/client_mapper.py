from src.domain.entities.client import ClientEntity
from src.presentation.rest.schemas.client_schema import IClientRead


class ClientMapper:
    @staticmethod
    def to_read_schema(domain: ClientEntity) -> IClientRead:
        return IClientRead(
            client_id=domain.id,
            login=domain.login,
            age=domain.age,
            location=domain.location,
            gender=domain.gender,
        )

    @staticmethod
    def to_domain(schema: IClientRead) -> ClientEntity:
        return ClientEntity(
            id=schema.client_id,
            login=schema.login,
            age=schema.age,
            location=schema.location,
            gender=schema.gender,
        )
