from pydantic import BaseModel


class IBanwordSettings(BaseModel):
    moderation: bool = False
