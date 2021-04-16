from fastapi import APIRouter

from utils.db_utils import connect_db

total_cost_router = APIRouter(prefix='/total_cost', tags=['total_cost'])


@total_cost_router.get('', tags=['total_cost'])
async def get_total_cost():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT SUM(amount * price) FROM resources")
    total = cur.fetchone()[0]
    return {'total_cost': total}
