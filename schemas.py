from pydantic import BaseModel, Field
from datetime import datetime


class BookPriceImageSchema(BaseModel):
    price: float = Field(ge=1)
    image: str = Field(examples=['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4-G0xMQ-fg6PjacmwwJngUyCqA5mRlBQVXDCiZiG4u8BXHM9cAfYrhGsaEP95KUBeI5O4QflcRwQi_ktoOG7myNDjDrVmT8njMZqHowNx&s=10'])


class BookCreateSchema(BookPriceImageSchema):
    title: str = Field(examples=['Я, легенда'])
    author: str = Field(examples=['Ричард Мэтисон'])


class BookSavedSchema(BookCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)