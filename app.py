import os

import psycopg2
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from endpoints.resources import resources_router
from endpoints.total_cost import total_cost_router

# Чтение переменных из .env файла
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = FastAPI()
con = psycopg2.connect(
    database=os.getenv('DATABASE'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    host="127.0.0.1", port="5432"
)
cur = con.cursor()

app.include_router(resources_router)
app.include_router(total_cost_router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True, debug=True, workers=3)
