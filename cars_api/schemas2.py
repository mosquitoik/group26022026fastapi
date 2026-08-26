from datetime import datetime

from pydantic import BaseModel, Field


class CarPatchSchema(BaseModel):
    price: float | None = Field(default=None, ge=1)
    color: str | None = None
    is_available: bool | None = None


class CarCreateSchema(CarPatchSchema):
    brand: str = Field(examples=["BMW"])
    model: str = Field(examples=["M5"])
    year: int = Field(ge=1886, examples=[2020])
    price: float = Field(ge=1, examples=[50000])
    color: str = Field(examples=["black"])
    is_available: bool = Field(default=True)


class CarSavedSchema(CarCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
