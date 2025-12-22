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

    percentage_change, high, low = get_daily_change(price_data)
    slope = get_trend(price_data)
    volatility, stability_score = get_volatility_and_stability(price_data)
    stability_label = get_stability_label(stability_score)
    ath, atl = get_ath_atl(price_data)
    total_volume, volume_24h = get_volume(price_data)
    percentage_changes = get_timeframe_percentage_change(price_data)
    #percentage_changes = ['1']

    stats = {
        "percentage_change": percentage_change,
        "daily_high": high,
        "daily_low": low,
        "trend_slope": slope,
        "volatility": volatility,
        "stability_score": stability_score,
        "stability_label": stability_label,
        "all_time_high": ath,
        "all_time_low": atl,
        "total_volume": total_volume,
        "volume_24h": volume_24h,
        "percentage_changes": percentage_changes,
    }

    return stats

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
    percentage_change = (f"{round(percentage_change, 2)}%")

    return percentage_change, highest_price, lowest_price

def get_trend(price_data):
    
    ts = np.array([convert_timestamp_unix(entry[0]) for entry in price_data], dtype=np.float64)
    prices = np.array([entry[1] for entry in price_data], dtype=np.float64)

    ts_days = ts / (1000 * 60 * 60 * 24)

    slope, intercept = np.polyfit(ts_days, prices, 1)
    slope = round(slope, 2)

    return slope

def get_volatility_and_stability(price_data):
    
    prices = np.array([entry[1] for entry in price_data], dtype=np.float64)
    returns = np.diff(np.log(prices))
    vol = np.std(returns)

    #reasonable estimate at a vol value that would be considered very unstable
    MAX_VOL = 0.05
    normalized_vol = vol/MAX_VOL
    normalized_vol = round(min(max(normalized_vol, 0), 1), 3)
    stability_score = round((1 - normalized_vol) * 100, 2)

    return normalized_vol, stability_score

def get_stability_label(stability):
    if stability is None or np.isinf(stability) or np.isnan(stability):
        return {
            "stability_label": "Insufficient data",
            "color": "gray"
        }

    if stability > 40:
        return "Very Stable"
    elif stability > 20:
        return "Stable"
    elif stability > 10:
        return "Moderate"
    elif stability > 5:
        return "Volatile"
    else:
        return "Very Volatile"


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
    '''
    It should be noted that volume is not possible in the traditional sense.
    This is a record of quantity loss over time, indicating that sales have occured (ie trades occured).
    But this is a record between 2 snapshots of quantity of an item in time, and cannot find every trade that has occured.
    If auctions are created and sold, this will not be known, as the API does not contain that data.
    '''
    parsed_data = []

    for entry in price_data:
         ts = entry[0]
         ts = datetime.fromisoformat(ts)
         quantity = entry[2]
         parsed_data.append((ts, quantity))

    now = parsed_data[-1][0]
    target_ts = now - timedelta(days=1)

    total_volume = 0
    volume_24h = 0

    previous_quantity = parsed_data[0][1]

    for ts, quantity in parsed_data[1:]:
        diff = previous_quantity - quantity

        if diff > 0:
            total_volume += diff

            if ts >= target_ts:
                volume_24h + diff

        previous_quantity = quantity

    return total_volume, volume_24h

def get_moving_average(price_data):

    filled_data = fill_missing_hours(price_data)
    prices = [entry[1] for entry in filled_data]

    window = 24
    weights = np.ones(window)/window
    ma = np.convolve(weights, prices, mode="valid")
    ts_ma = [t for t, _ in filled_data][window-1:]

    return (ts_ma, ma)

def fill_missing_hours(price_data):
    data = [(datetime.fromisoformat(entry[0]), entry[1]) for entry in price_data]
    
    filled = []
    start_time = data[0][0]
    end_time = data[-1][0]
    idx = 0
    last_price = data[0][1]

    while start_time <= end_time:
        if idx < len(data) and data[idx][0] == start_time:
            last_price = data[idx][1]
            idx += 1
        filled.append((start_time, last_price))
        start_time += timedelta(hours=1)
    
    return filled

def get_timeframe_percentage_change(price_data):

    now_ts = datetime.fromisoformat(price_data[-1][0])
    first_ts = datetime.fromisoformat(price_data[0][0])
    timeframes = {
        "1w": now_ts - timedelta(weeks=1),
        "1m": now_ts - timedelta(days=30),
        "1y": now_ts - timedelta(weeks=52),
        "all": first_ts
    }
    percentage_changes = {}
    
    for label, target_ts in timeframes.items():

        closest_diff = None
        closest_entry = None

        for entry in price_data:
            ts = datetime.fromisoformat(entry[0])
            difference = abs(target_ts - ts)

            if closest_diff is None or difference < closest_diff:
                closest_diff = difference
                closest_entry = entry
        
        now_price = price_data[-1][1]
        previous_price = closest_entry[1]

        percentage_change = (now_price - previous_price)/previous_price * 100
        percentage_changes[label] = (f"{round(percentage_change, 2)}%")
    
    return percentage_changes
