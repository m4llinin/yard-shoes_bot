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


class AmoCRM:
    pipeline_id = 612907
    field_names = (
        "Крой Перфорация Покраска Заготовка Адаптация колодки Затяжка Рант и подошва Прошивка Каблук Финиш Упаковка")

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
                    raise None
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
                    raise None
        except aiohttp.ClientError:
            return None

# asyncio.run(AmoCRM.find_order("Пр: М10065"))
# asyncio.run(AmoCRM.get_specialists())
