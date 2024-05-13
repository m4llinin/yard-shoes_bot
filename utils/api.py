import asyncio
import aiohttp

from dataclasses import dataclass
from typing import List
from config import config


@dataclass
class Specialist:
    id: int
    name: str


@dataclass
class Step:
    id: int
    title: str
    specialists: List[Specialist]


@dataclass
class Choice:
    work_id: int
    work: str
    specialist_id: str


class AmoCRM:
    pipeline_id = 612907
    field_names = (
        "Крой Перфорация Покраска Заготовка Адаптация колодки Затяжка Рант и подошва Прошивка Каблук Финиш Упаковка")
    field_date = (
        "Дата кроя Дата перфорации Дата покраски Дата заготовки Дата адаптации Дата затяжки Дата рант и подошва"
        " Дата прошивки Дата каблука Дата финиша Дата отправки Дата упаковки")

    headers = {
        'Authorization': f'Bearer {config.AmoCRM}'
    }

    @classmethod
    async def find_order(cls, name_order: str) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://yardshoes.amocrm.ru/api/v4/leads?filter[name]={name_order}",
                                       headers=cls.headers) as response:
                    data = await response.json()
                    if response.status == 200:
                        return data['_embedded']['leads'][0]
                    return None
        except aiohttp.ClientError:
            return None

    @classmethod
    async def get_specialists(cls) -> List[Step]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://yardshoes.amocrm.ru/api/v4/leads/custom_fields",
                                       headers=cls.headers) as response:
                    data = await response.json()
                    if response.status == 200:
                        steps = []
                        for field in data['_embedded']['custom_fields']:
                            if field['name'] in cls.field_names:
                                if field["enums"] and field["code"] != '':
                                    arr = [Specialist(f["id"], f["value"]) for f in field['enums']]
                                    steps.append(Step(field["id"], field['name'], arr))
                        return steps
                    return None
        except aiohttp.ClientError:
            return None

    @classmethod
    async def find_date(cls, work: str) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://yardshoes.amocrm.ru/api/v4/leads/custom_fields",
                                       headers=cls.headers) as response:
                    data = await response.json()
                    if response.status == 200:
                        for field in data['_embedded']['custom_fields']:
                            name = field['name']
                            if name in cls.field_date and work.lower().rsplit(" ")[0][:-1] in name:
                                return field
                    return None
        except aiohttp.ClientError:
            return None

    @classmethod
    async def get_next_status(cls, pipeline_id: int, cur_status: int) -> int:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://yardshoes.amocrm.ru/api/v4/leads/pipelines/{pipeline_id}/statuses",
                                       headers=cls.headers) as response:
                    data = await response.json()
                    if response.status == 200:
                        for i in range(len(data["_embedded"]["statuses"])):
                            if data["_embedded"]["statuses"][i]['id'] == cur_status:
                                return data["_embedded"]["statuses"][i + 1]['id']
                    return None
        except (aiohttp.ClientError, IndexError):
            return None

    @classmethod
    async def update_orders(cls, work_id: int, enum_id: str, date_id: int, data_value: float, orders: list) -> list:
        data = {
            "custom_fields_values": [
                {
                    "field_id": date_id,
                    "values": [
                        {
                            "value": int(data_value)
                        }
                    ]
                },
                {
                    "field_id": work_id,
                    "values": [
                        {
                            "value": enum_id
                        }
                    ]
                }
            ]
        }

        result = []
        for order in orders:
            next_st = await cls.get_next_status(order["pipeline_id"], order['status_id'])
            if next_st:
                data['status_id'] = next_st
            async with aiohttp.ClientSession() as session:
                cls.headers["Content-Type"] = "application/json"
                async with session.patch(f"https://yardshoes.amocrm.ru/api/v4/leads/{order['id']}",
                                         headers=cls.headers,
                                         json=data) as response:
                    if response.status == 200:
                        result.append((order['name'], 1))
                    else:
                        result.append((order['name'], 0))
            del data['status_id']
        return result

# asyncio.run(AmoCRM.find_order("Пр: М10065"))
