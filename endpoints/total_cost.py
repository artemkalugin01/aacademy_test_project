import os

import psycopg2
from fastapi import APIRouter

total_cost_router = APIRouter(prefix='/total_cost', tags=['total_cost'])


@total_cost_router.get('', tags=['total_cost'])
async def get_total_cost():
    con = psycopg2.connect(database=os.getenv('DATABASE'), user=os.getenv('USER'), password=os.getenv('PASSWORD'),
                           host=os.getenv('HOST'), port=os.getenv('PORT'))
    cur = con.cursor()
    cur.execute("SELECT SUM(amount * price) FROM resources")
    total = cur.fetchone()[0]
    return {'total_cost': total}
