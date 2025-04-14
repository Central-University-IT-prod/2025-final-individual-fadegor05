from uuid import UUID

from pydantic import BaseModel

from src.core.fields import ScoreField


class IMLScoreRead(BaseModel):
    client_id: UUID
    advertiser_id: UUID
    score: ScoreField
