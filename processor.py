import json
import statistics
import numpy as np
from collections import defaultdict
from fetch import get_item_info_by_id
from datetime import datetime, timezone, timedelta
from storage import get_prices_for_item

def normalise_auction(auction):
    buyout_price = auction.get("buyout")
    quantity = auction.get("quantity", 1)
    
    if not buyout_price or quantity == 0:
        return None

    unit_price = buyout_price / quantity

    return {
        "id": auction["item"]["id"],
        "unit_price": unit_price,
        "quantity": quantity
    }

    
def normalise_auction_commodities(auction):
    quantity = auction.get("quantity", 1)
    unit_price = auction.get("unit_price")

    if unit_price is None or quantity == 0:
        return None

    buyout_price = unit_price * quantity

    return {
        "id": auction["item"]["id"],
        "unit_price": unit_price,
        "quantity": quantity,
        "buyout_price": buyout_price
    }



def group_auctions_by_item_id(normalised_auctions):
    price_map = defaultdict(lambda: {"prices": [], "quantity": 0})

    for auction in normalised_auctions:
        if auction is None:
            continue
        item_id = auction["id"]
        price_map[item_id]["prices"].append(auction["unit_price"])
        price_map[item_id]["quantity"] += auction["quantity"]

    return price_map


def calculate_median(price_map):
    medians = {}
    for item_id, data in price_map.items():
        median_price = statistics.median(data["prices"])
        medians[item_id] = {
            "median": median_price,
            "quantity": data["quantity"]
        }
    return medians

def compute_item_medians(data):

    normalised_auctions = []
    for auction in data['auctions']:
        normalised_auctions.append(normalise_auction(auction))

    price_map = group_auctions_by_item_id(normalised_auctions)
    medians = calculate_median(price_map)

    return medians

def compute_commodities_medians(data):
    
    normalised_auctions = []
    for auction in data['auctions']:
        normalised_auctions.append(normalise_auction_commodities(auction))

    price_map = group_auctions_by_item_id(normalised_auctions)
    medians = calculate_median(price_map)

    return medians

def get_item_name_from_id(item_id):
    item_info = get_item_info_by_id(item_id)
    if item_info and "name" in item_info:
        return item_info["name"]
    return None

def convert_price(price):

    gold = price // 10000
    silver = (price % 10000) // 100
    copper = ((price % 10000) % 100) // 100

    print(f"{gold}g {silver}s {copper}c")

    return gold, silver, copper

def convert_timestamp(timestamp):

    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%H:%m/%d")

def convert_timestamp_unix(ts_str: str) -> int:
    dt = datetime.fromisoformat(ts_str)
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)

def calculate_stats(price_data):
    percentage_change = get_daily_change(price_data)
    slope = get_trend(price_data)
    volatility = get_volatility(price_data)
    ath, atl = get_ath_atl(price_data)

    return percentage_change, slope, volatility, ath, atl

def get_daily_change(price_data):
    now_ts = datetime.fromisoformat(price_data[-1][0])

    target_ts = now_ts - timedelta(days=1)

    closest_diff = None
    closest_entry = None
    highest_price = None
    lowest_price = None

    for entry in price_data:
        ts = datetime.fromisoformat(entry[0])
        price = entry[1]
        difference = abs(target_ts - ts)

        if closest_diff is None or difference < closest_diff:
            closest_diff = difference
            closest_entry = entry
    
    start_index = price_data.index(closest_entry)

    for entry in price_data[start_index:]:
        price = entry[1]
        
        if highest_price is None or price > highest_price:
            highest_price = price

        if lowest_price is None or price < lowest_price:
            lowest_price = price
    
    now_price = price_data[-1][1]
    previous_price = closest_entry[1]

    percentage_change = (now_price - previous_price)/previous_price * 100

    return percentage_change, highest_price, lowest_price

def get_trend(price_data):

    if len(price_data) < 2:
        return None
    
    ts = np.array([convert_timestamp_unix(entry[0]) for entry in price_data], dtype=np.float64)
    prices = np.array([entry[1] for entry in price_data], dtype=np.float64)

    ts_days = ts / (1000 * 60 * 60 * 24)

    slope, intercept = np.polyfit(ts_days, prices, 1)

    return slope

def get_volatility(price_data):

    if len(price_data) < 2:
        return None
    
    prices = np.array([entry[1] for entry in price_data], dtype=np.float64)
    returns = np.diff(np.log(prices))
    vol = np.std(returns)

    return vol

def get_ath_atl(price_data):

    ath = None
    atl = None

    for entry in price_data:
        if ath is None or entry[1] > ath:
            ath = entry[1]

        if atl is None or entry[1] < atl:
            atl = entry[1]

    return ath, atl

def get_volume(price_data):

    volume = None
    twenty_four_h_volume = None

    for entry in price_data:
         volume = entry[2]

    return volume