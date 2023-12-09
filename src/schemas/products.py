from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(read_only=True)
    name: str
    description: str
    price: float
    image: str | None
    stock: int | None
