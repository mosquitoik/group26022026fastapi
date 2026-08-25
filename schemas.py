from pydantic import BaseModel, Field
from datetime import datetime


class BookCreateSchema(BaseModel):
    title: str = Field(default='Я, легенда')
    image: str = Field(default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4-G0xMQ-fg6PjacmwwJngUyCqA5mRlBQVXDCiZiG4u8BXHM9cAfYrhGsaEP95KUBeI5O4QflcRwQi_ktoOG7myNDjDrVmT8njMZqHowNx&s=10')
    price: float = Field(ge=1)
    author: str = Field(default='Ричард Мэтисон')


class BookSavedSchema(BookCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)