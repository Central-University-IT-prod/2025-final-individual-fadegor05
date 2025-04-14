import pytest
from pydantic import BaseModel

from src.core.enums import AllGenderEnum
from src.domain.value_objects.targeting import Targeting
from src.presentation.rest.mappers.targeting_mapper import TargetingMapper
from src.presentation.rest.schemas.targeting_schema import ITargetRead


class MockITargetRead(BaseModel):
    gender: AllGenderEnum | None = None
    age_from: int | None = None
    age_to: int | None = None
    location: str | None = None


@pytest.fixture
def domain_targeting():
    return Targeting(
        gender=AllGenderEnum.MALE, age_from=25, age_to=35, location="New York"
    )


@pytest.fixture
def schema_targeting():
    return MockITargetRead(
        gender=AllGenderEnum.MALE, age_from=25, age_to=35, location="New York"
    )


def test_to_read_schema(domain_targeting):
    schema = TargetingMapper.to_read_schema(domain_targeting)
    assert schema.gender == domain_targeting.gender
    assert schema.age_from == domain_targeting.age_from
    assert schema.age_to == domain_targeting.age_to
    assert schema.location == domain_targeting.location
    assert isinstance(schema, ITargetRead)  # Check correct type


def test_to_domain(schema_targeting):
    domain = TargetingMapper.to_domain(schema_targeting)
    assert domain.gender == schema_targeting.gender
    assert domain.age_from == schema_targeting.age_from
    assert domain.age_to == schema_targeting.age_to
    assert domain.location == schema_targeting.location
    assert isinstance(domain, Targeting)


def test_to_read_schema_none_values():
    domain = Targeting()
    schema = TargetingMapper.to_read_schema(domain)
    assert schema.gender is None
    assert schema.age_from is None
    assert schema.age_to is None
    assert schema.location is None


def test_to_domain_none_values():
    schema = MockITargetRead()
    domain = TargetingMapper.to_domain(schema)
    assert domain.gender is None
    assert domain.age_from is None
    assert domain.age_to is None
    assert domain.location is None


def test_to_read_schema_different_gender(domain_targeting):
    domain_targeting.gender = AllGenderEnum.FEMALE
    schema = TargetingMapper.to_read_schema(domain_targeting)
    assert schema.gender == AllGenderEnum.FEMALE

    domain_targeting.gender = AllGenderEnum.ALL
    schema = TargetingMapper.to_read_schema(domain_targeting)
    assert schema.gender == AllGenderEnum.ALL


def test_to_domain_different_gender(schema_targeting):
    schema_targeting.gender = AllGenderEnum.FEMALE
    domain = TargetingMapper.to_domain(schema_targeting)
    assert domain.gender == AllGenderEnum.FEMALE

    schema_targeting.gender = AllGenderEnum.ALL
    domain = TargetingMapper.to_domain(schema_targeting)
    assert domain.gender == AllGenderEnum.ALL


def test_to_read_schema_different_ages(domain_targeting):
    domain_targeting.age_from = 18
    domain_targeting.age_to = 65
    schema = TargetingMapper.to_read_schema(domain_targeting)
    assert schema.age_from == 18
    assert schema.age_to == 65


def test_to_domain_different_ages(schema_targeting):
    schema_targeting.age_from = 18
    schema_targeting.age_to = 65
    domain = TargetingMapper.to_domain(schema_targeting)
    assert domain.age_from == 18
    assert domain.age_to == 65


def test_to_read_schema_different_locations(domain_targeting):
    domain_targeting.location = "London"
    schema = TargetingMapper.to_read_schema(domain_targeting)
    assert schema.location == "London"


def test_to_domain_different_locations(schema_targeting):
    schema_targeting.location = "London"
    domain = TargetingMapper.to_domain(schema_targeting)
    assert domain.location == "London"


def test_to_read_schema_and_back(domain_targeting):
    schema = TargetingMapper.to_read_schema(domain_targeting)
    domain2 = TargetingMapper.to_domain(schema)
    assert domain2 == domain_targeting


def test_to_domain_and_back(schema_targeting):
    domain = TargetingMapper.to_domain(schema_targeting)
    schema2 = TargetingMapper.to_read_schema(domain)

    assert schema2.gender == schema_targeting.gender
    assert schema2.age_to == schema_targeting.age_to
    assert schema2.age_from == schema_targeting.age_from
    assert schema2.location == schema_targeting.location
