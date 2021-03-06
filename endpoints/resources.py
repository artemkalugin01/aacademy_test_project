import datetime

from fastapi import APIRouter

from models.resource import Resource
from utils.db_utils import connect_db

"""
колонны таблицы resources в PostgreSQL
По сравнению с моделью Pydantic отсутствуют:
id: так как тип в БД BIGSERIAL = автоувеличение + создаётся автоматически
cost: нет смысла хранить так как высчитывается из известных параметров
"""
resources_columns = '(title, amount, unit, price, date)'
resources_router = APIRouter(prefix='/resources', tags=['resources'])


@resources_router.get('', tags=['resources'])
async def get_resources():
    con = connect_db()
    cur = con.cursor()

    cur.execute('SELECT * FROM resources')
    resources = cur.fetchall()
    con.close()
    d = {}
    res_lst = []
    for res in resources:
        res_lst.append(Resource.parse_from_db(res))
    d['resources'] = res_lst
    d['total_count'] = len(res_lst)
    return d


@resources_router.post('', tags=['resources'])
async def post_resources(resource: Resource):
    con = connect_db()
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO resources {resources_columns} VALUES ('{resource.title}', {resource.amount}, '{resource.unit}',"
        f" {resource.price}, '{resource.date}') RETURNING *")

    con.commit()
    con.close()
    return resource.dict(exclude={'id', 'cost'})


@resources_router.delete('', tags=['resources'])
async def delete_resources(id: int):
    con = connect_db()
    cur = con.cursor()

    cur.execute(f"DELETE FROM resources WHERE id={id}")
    con.commit()
    con.close()


@resources_router.put('', tags=['resources'])
async def put_resources(id: int, amount: float, price: float, date: datetime.date, title: str, unit: str):
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        f"UPDATE resources SET {resources_columns} = ('{title}', {amount}, '{unit}', {price}, '{date}') WHERE id={id}")

    con.commit()
    con.close()
