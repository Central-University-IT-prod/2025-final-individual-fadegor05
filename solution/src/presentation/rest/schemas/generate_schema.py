from pydantic import BaseModel


class IGenerateTextCreate(BaseModel):
    title: str


class IGenerateTextRead(IGenerateTextCreate):
    text: str


class IGenerateImageCreate(BaseModel):
    title: str
    text: str
