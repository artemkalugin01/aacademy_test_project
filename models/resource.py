import pydantic
from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class Resource(BaseModel):
    """
    Модель данных Resource используемая в задании
    """
    title: str
    id: Optional[int] = -1
    amount: float
    unit: str
    price: float
    cost: Optional[float] = 0
    date: date

    @pydantic.validator('cost', pre=True, always=True)
    def default_ts_modified(cls, v, *, values, **kwargs):
        """
        Валидатор, присваивающий значение полю cost исходя из параметров amount & price
        :param v: значение если передано, записывается без высчитывания
        :param values: поля
        :param kwargs:
        :return:
        """
        return v or float(values['amount'] * values['price'])

    @staticmethod
    def parse_from_db(values: List):
        """
        Вспомогательный метод чтения из БД
        :param values: Лист параметров, возвращённый из БД
        :return:
        """
        r = Resource(id=values[0], title=values[1], amount=values[2], unit=values[3], price=values[4], date=values[5])
        return r

    class Config:
        schema_extra = {
            "example resource": {
                "title": "str",
                "amount": "float",
                "unit": "str",
                "price": "float",
                "date": "date"
            }
        }
