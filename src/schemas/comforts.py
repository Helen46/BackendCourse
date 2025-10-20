from datetime import date

from pydantic import BaseModel, Field


class ComfortAdd(BaseModel):
    title: str


class Comfort(ComfortAdd):
    id: int