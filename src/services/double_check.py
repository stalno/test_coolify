import httpx
import json
from typing import List
from collections import Counter
from datetime import datetime


import mimetypes
from pathlib import Path

from poetry.vcs.git.backend import logger

RETAILCRM_API_URL = "https://radis.retailcrm.ru/api/v5"
RETAILCRM_API_KEY = "KSfksBmD3beM4eEVkCus6B9VEsPnmUIU"

async def get_orders_by_filter():
    page = 1

    async with httpx.AsyncClient() as client:
        params = {
            "filter[orderMethods][]": ["lid-from-adanilchik"],
            "filter[customFields][]": ["id_zakaza"],
            "apiKey": RETAILCRM_API_KEY,
            "limit": 100, "page": page
        }
        response = await client.get(f"{RETAILCRM_API_URL}/orders", params=params)

        total_pages = response.json().get("pagination", {}).get("totalPageCount")
        orders = response.json().get("orders", [])
        total_order_nums = [order.get("number") for order in orders]
        while True:
            params = {
                "filter[orderMethods][]": ["lid-from-adanilchik"],
                "filter[customFields][]": ["id_zakaza"],
                "apiKey": RETAILCRM_API_KEY,
                "limit": 100, "page": page
            }
            total_order_nums = []

            print("\n", params["page"])
            response = await client.get(f"{RETAILCRM_API_URL}/orders", params=params)
            current_page = response.json().get("pagination", {}).get("currentPage")
            orders = response.json().get("orders", [])
            for order in orders:
                total_order_nums.append(order.get("number"))

            count = Counter(total_order_nums)
            duplicates = [number for number, freq in count.items() if freq > 1]

            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            for number in duplicates:
                param = {"filter[numbers][]": [number], "apiKey": RETAILCRM_API_KEY}
                response = await client.get(f"{RETAILCRM_API_URL}/orders", params=param)
                orders = response.json().get("orders", [])
                id_list = ([{"id": item["id"], "site": item["site"]} for item in orders])[1:]
                print(id_list)

                for el in id_list:
                    new_order = {"managerId": 53}
                    data = {"by": "id", "order": json.dumps(new_order), 'apiKey': RETAILCRM_API_KEY, "site": el["site"]}
                    id = el.get("id")
                    result = await client.post(
                        url=RETAILCRM_API_URL + f"/orders/{id}/edit",
                        data=data,
                        headers=headers
                    )
                    print(result.json())
            if total_pages == current_page:
                break
            page += 1

        # count = Counter(total_order_nums)
        # duplicates = [number for number, freq in count.items() if freq > 1]
        #
        # headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # for number in duplicates:
        #     params["filter[numbers][]"] = [number]
        #     response = await client.get(f"{RETAILCRM_API_URL}/orders", params=params)
        #     orders = response.json().get("orders", [])
        #     id_list = ([{"id": item["id"], "site": item["site"]} for item in orders])[1:]
        #     print(id_list)
        #
        #     for el in id_list:
        #         new_order = {"managerId": 53}
        #         data = {"by": "id", "order": json.dumps(new_order), 'apiKey': RETAILCRM_API_KEY, "site": el["site"]}
        #         id = el.get("id")
        #         result = await client.post(
        #             url=RETAILCRM_API_URL+f"/orders/{id}/edit",
        #             data=data,
        #             headers=headers
        #         )
        #         print(result.json())

        return total_order_nums

async def get_ids():
    url = "https://emiliemusee.retailcrm.ru/api/v5/store/offers"
    async with httpx.AsyncClient() as client:
        current_page = 1
        while True:
            params = {"apiKey": "tm6OOPF74KpBR4twABIwQGJNjpBm4zkD", "limit": 100, "page": current_page}
            response = await client.get(url, params=params)
            ids = []
            for el in response.json().get("offers"):
                ids.append(el.get("id"))
            results = await changed_price(ids = ids)
            if results:
                current_page += 1
                print(current_page, results)
                await asyncio.sleep(3)


async def changed_price(ids: List[int]):
    prices = []
    for id in ids:
        data = {"id": id, "site":"emiliemusee-ru", "prices": [{"code":"aktsionnaia", "remove":True}]}
        prices.append(data)
    new_data = {"prices": json.dumps(prices),
                "apiKey": "tm6OOPF74KpBR4twABIwQGJNjpBm4zkD"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = f"https://emiliemusee.retailcrm.ru/api/v5/store/prices/upload"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=new_data, headers=headers)
        if response.status_code == 200:
            if response.json().get("processedOffersCount"):
                logger.info(f"Все хорошо {response.json()}")

                return response.json()
            else:
                logger.warning(f"Что то не так: {response.json()}")
        else:
            logger.error(f"Проверь {response.json()}")


async def get_history_rebox():
    host = "https://rebox.retailcrm.ru" + '/api/v5/orders/history'
    #history_id = 1210014
    params = {'apiKey': "QVV6JOmecHIguHsOlkTN3RiuuCUZVQA6"}
    #params['filter[sinceId]'] = history_id

    async with httpx.AsyncClient() as client:
        # current_page = 1
        # params['page'] = current_page
        payload = await client.get(url=host, params=params)
        response = payload.json()
        last_page = response.get("pagination", {}).get("totalPageCount")
        params['page'] = last_page - 100
        params['filter[endDate]'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = await client.get(url=host, params=params)
        data = response.json()
        print(response)


async def get_last_client_id_by_mango_client():
    url = "https://lusio.retailcrm.ru/api/v5/customers"
    params = {
        'apiKey': "sC28YRrHrqAHHPNRnko01FUWTfd62wpc",
        "limit": 100,
              }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        ids = []
        if response.status_code == 200:
            data = response.json()
            for customer in data.get("customers"):
                if customer.get("lastClientId"):
                    ids.append(customer.get("lastClientId"))
        res =  set(ids)
        return res


async def get_last_client_id_from_order():
    url = "https://lusio.retailcrm.ru/api/v5/orders"
    params = {
        'apiKey': "sC28YRrHrqAHHPNRnko01FUWTfd62wpc",
        "limit": 100,
        "filter[sites][]": ["lusio-ru"]
              }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        ids = []
        if response.status_code == 200:
            data = response.json()
            for order in data.get("orders"):
                if order.get("customer", {}).get("lastClientId"):
                    ids.append(order.get("customer", {}).get("lastClientId"))
        res =  set(ids)
        return res


async def get_order_by_id(url: str, id: int, api_key: str):
    url = f"{url}/api/v5/orders/{id}"
    params = {"apiKey": api_key, "by":"id"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        order = response.json().get("order")
        return order



async def upload_file():
    url = "https://seafood-shop3.retailcrm.ru/api/v5/files/upload"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {"apiKey": "TxVe4LpdAmpwziDSzbQ92TedWuVDnaOL"}

    file_path = "/Users/a1111/Documents/Picture/Оригинал 1600x1200.jpg"
    # Определяем MIME-тип файла
    # mime_type, _ = mimetypes.guess_type(file_path)
    # if not mime_type:
    mime_type = "application/octet-stream"

    # Получаем имя файла из пути
    file_name = Path(file_path).name

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Открываем файл в бинарном режиме
            with open(file_path, "rb") as f:
                files = {"file": (file_name, f, mime_type)}

                # Отправляем асинхронный запрос
                response = await client.post(
                    url,
                    params=params,
                    files=files,
                    headers=headers
                )

            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            return {
                "success": False,
                "errorMsg": f"HTTP error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "errorMsg": f"Unexpected error: {str(e)}"
            }

async def update_order():
    order = {
"status": "cancel-other",
"items": [
{
"markingCodes": [
# "0104607097019289215N1u/LsL'E'ip\x1d91EE10\x1d92aps40dC6s44bXljrly36JPDbnXxRNXAluwngS0xjmvU=",
# "0104607097019289215v!6GtrqYLYmG\x1d91EE10\x1d929I/EsgPmzng0CWRABwkeiPf2vKV0GVBPNZUmxHTZcwI="
],
"externalIds": [
{
"value": "f7d87821-68ac-4027-90ca-3d80c512065f",
"code": "1C"
}
],
"discountManualAmount": 0,
"quantity": 2,
"initialPrice": 620,
"id": "460",
"discountManualPercent": 0,
"productName": "\u0412\u0438\u0442\u0430\u043C\u0438\u043D D3, 450 \u043C\u0433, 120 \u043A\u0430\u043F\u0441\u0443\u043B QR",
"status": "failure",
"offer": {
"xmlId": "8894c3d2-e9be-11ed-8110-0cc47ae051d5"
}
},
{
"markingCodes": [],
"externalIds": [
{
"value": "ca225fa0-1fa0-4daf-9ab2-dc6e9414430d",
"code": "1C"
}
],
"discountManualAmount": 0,
"quantity": 1,
"initialPrice": 2250,
"id": "461",
"discountManualPercent": 0,
"productName": "\u0418\u043A\u0440\u0430 \u0424\u041E\u0420\u0415\u041B\u0418 \u043F\u043B\/\u0431 200\u0433",
"status": "failure",
"offer": {
"xmlId": "1454d05d-4300-11e8-9e3b-001dd8b89db0"
}
}
]
}
    url = "https://seafood-shop3.retailcrm.ru/api/v5/orders/249/edit"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    body = {"order": json.dumps(order), "by": "id", "apiKey": "UG4RpmHiFDjN4tPXHEpEVJdTEOiSkDgH", "site": "seafood-shop3"}
    params = {"apiKey": "UG4RpmHiFDjN4tPXHEpEVJdTEOiSkDgH", "site": "seafood-shop3"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=body)
        result = response.json()
        return result





async def main():
    #await get_orders_by_filter()
    #await get_ids()
    #await get_history_rebox()
    #await get_last_client_id_by_mango_client()
    await get_last_client_id_from_order()
    #await get_order_by_id(url="https://purpur.retailcrm.ru", id=3970, api_key="5L7THru0CnNEC69arCaz8KDWzFV8TLm8" )
    #await upload_file()
    #await update_order()
    #await get_order_by_id(url="https://seafood-shop3.retailcrm.ru", api_key="UG4RpmHiFDjN4tPXHEpEVJdTEOiSkDgH", id=249)
#     data1 = {"markingCodes": [
# "0104607097019289215N1u/LsL'E'ip\x1d91EE10\x1d92aps40dC6s44bXljrly36JPDbnXxRNXAluwngS0xjmvU=",
# "0104607097019289215v!6GtrqYLYmG\x1d91EE10\x1d929I/EsgPmzng0CWRABwkeiPf2vKV0GVBPNZUmxHTZcwI="
# ]}
#     data2 = {"markingCodes": [
# "0104607097019289215N1u/LsL'E'ip\u001D91EE10\u001D92aps40dC6s44bXljrly36JPDbnXxRNXAluwngS0xjmvU=",
# "0104607097019289215v!6GtrqYLYmG\x1d91EE10\x1d929I/EsgPmzng0CWRABwkeiPf2vKV0GVBPNZUmxHTZcwI="
# ]}


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())