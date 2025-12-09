from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storage import get_prices_for_item
from processor import convert_timestamp_unix
from typing import Optional
from datetime import datetime, timezone
from storage import get_item_name_from_db

app = FastAPI()

origins = [
    "https://127.0.0.1/:5500",
    "http://127.0.0.1:5500",
    "https://127.0.0.1",
    "http://127.0.0.1",
    "https://127.0.0.1:8080",
    "http://127.0.0.1:8080",
    "https://127.0.0.1:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/name/{item_id}")
async def get_item_name(item_id: int):
    name = get_item_name_from_db(item_id)

    return {"name": name}

@app.get("/data")
async def ah_prices(
    item_id: int,
    start: Optional[str] = None,
    end: Optional[str] = None
    ):

    #item_id = 2770
    data = get_prices_for_item(item_id)

    results = []

    for timestamp, price in data:
        timestamp = convert_timestamp_unix(timestamp)

        if start:
            start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
            if timestamp < int(start_dt.timestamp() * 1000):
                continue

        if end:
            end_dt = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
            if timestamp > int(end_dt.timestamp() * 1000):
                continue

        results.append({"t": timestamp, "price": price})

    return {
        "item_id": item_id,
        "data": results
    }