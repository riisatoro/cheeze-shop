from pydantic import BaseModel


class OrderDetails(BaseModel):
    product_id: int
    quantity: int


class Order(BaseModel):
    id: int
    request_id: str
