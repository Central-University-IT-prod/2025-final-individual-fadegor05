from src.core.pagination import Pagination
from src.presentation.rest.schemas.common_schema import IPaginationCommon


class PaginationMapper:
    @staticmethod
    def to_domain(schema: IPaginationCommon) -> Pagination:
        return Pagination(limit=schema.size, offset=schema.size * schema.page)
