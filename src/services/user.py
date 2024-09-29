import json
import httpx

from src.common.constants import RETAILCRM_API_URL
from src.common.dto import (
    CustomerFilter,
    CustomerCreate,
    CreateOrderWithCustomerData,
)
import src.core.settings as settings
from src.services.base import BaseHttpService


class UserService(BaseHttpService):

    def __init__(self):
        super().__init__(base_url=RETAILCRM_API_URL, api_key=settings.RETAILCRM_API_KEY)

    async def get_customers_from_retailcrm(
        self, filters: CustomerFilter
    ) -> httpx.Response:
        params = {
            "filter[name]": filters.name,
            "filter[email]": filters.email,
        }
        if filters.registered_from:
            params["filter[dateFrom]"] = filters.registered_from
        if filters.registered_to:
            params["filter[dateTo]"] = filters.registered_to

        result = await self._get(endpoint="/customers", params=params)

        return result

    async def create_customer(
        self, customer_data: CustomerCreate
    ) -> httpx.Response:
        data = {
            "customer": json.dumps(
                {
                    "type": "customer",
                    "site": customer_data.site,
                    "externalId": customer_data.externalId,
                    "isContact": customer_data.isContact,
                    "vip": customer_data.vip,
                    "bad": customer_data.bad,
                    "contragent": {
                        "contragentType": customer_data.contragent.value,
                        "legalName": customer_data.contragent_legalName,
                    },
                    "address": {
                        "countryIso": customer_data.countryIso,
                        "city": customer_data.city,
                        "street": customer_data.street,
                        "building": customer_data.building,
                        "flat": customer_data.flat,
                        "text": customer_data.text,
                    },
                    "firstName": customer_data.firstName,
                    "lastName": customer_data.lastName,
                    "patronymic": customer_data.patronymic or "",
                    "email": customer_data.email,
                }
            )
        }

        return await self._post("/customers/create", data=data)

    async def get_order_by_customer_id(self, customer_id: int) -> httpx.Response:
        params = {"filter[customerId]": customer_id}
        return await self._get("/orders", params=params)

    async def create_order_with_customer_data(self, query: CreateOrderWithCustomerData) -> httpx.Response:
        data = {
            "order": json.dumps(
                {
                    "customer": {"id": query.customer_id},
                    "number": query.number,
                    "items": [{"productName": query.product_name}],
                }
            )
        }

        return await self._post("/orders/create", data=data)
