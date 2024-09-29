from enum import Enum
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class CustomerFilter(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    registered_from: Optional[date] = None
    registered_to: Optional[date] = None


class ContragentTypeQuery(Enum):
    INDIVIDUAL = "individual"
    LEGAL_ENTITY = "legal-entity"
    ENTERPRENEUR = "enterpreneur"


class CustomerCreate(BaseModel):
    externalId: str = Field(default="124456457675")
    isContact: bool = Field(default=False)
    site: str = Field(default="DEMO")
    vip: bool = Field(default=True)
    bad: bool = Field(default=False)
    firstName: str
    lastName: str
    patronymic: Optional[str] = None
    email: str
    contragent: ContragentTypeQuery
    contragent_legalName: Optional[str] = None
    contragent_legalAddress: Optional[str] = None
    countryIso: str = Field(default="RU")
    city: str = Field(default="Moscow")
    street: str = Field(default="Zarechnaya")
    building: str = Field(default="Wal")
    flat: str = Field(default="4")
    text: str = Field(default="Have a GOOD DAY!!!!!")

    class Config:
        use_enum_value = True


class CustomerID(BaseModel):
    customer_id: int


class CreateOrderWithCustomerData(CustomerID):
    number: str = Field(default="45382057914")
    product_name: str = Field(default="MacBook Air M1 16/256")
