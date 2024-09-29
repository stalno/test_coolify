from pydantic import BaseModel, Field


class CreateOrderWithCustomerData(BaseModel):
    customer_id: int
    number: str = Field(default="45382057914")
    product_name: str = Field(default="MacBook Air M1 16/256")