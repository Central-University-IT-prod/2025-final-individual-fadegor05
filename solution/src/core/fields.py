from typing import Annotated

from pydantic import Field, StringConstraints

NameField = Annotated[str, StringConstraints()]

LoginField = Annotated[str, StringConstraints()]

AgeField = Annotated[int, Field(ge=0)]

LocationField = Annotated[str, StringConstraints()]

ScoreField = Annotated[int, Field(ge=0)]

CountField = Annotated[int, Field(ge=0)]

CostField = Annotated[float, Field(ge=0)]

DateField = Annotated[int, Field(ge=0)]

LimitField = Annotated[int, Field(ge=0)]

AdTextField = Annotated[str, StringConstraints()]
