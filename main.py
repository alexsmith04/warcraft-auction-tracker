from datetime import datetime
from fetch import get_auctions_for_realm, get_item_info_by_id, get_commodities
from processor import compute_item_medians, get_item_name_from_id, compute_commodities_medians
from storage import init_db, insert_median_price, get_item_name_from_db, upsert_item_name

def run_once():
    init_db()
    print("database initialised")

    data = get_auctions_for_realm()
    print("got data")

    items_medians = compute_item_medians(data)
    print("medians calculated")
    
    commodities = get_commodities()
    print("got commodoites")

    commodities_medians = compute_commodities_medians(commodities)
    print("commodities medians calculated")

    medians = items_medians | commodities_medians

    timestamp = datetime.utcnow().isoformat()

    for item_id, median_price in medians.items():

        name = get_item_name_from_db(item_id)

        if not name:
            item_info = get_item_info_by_id(item_id)
            if item_info and "name" in item_info:
                name = item_info["name"]
                upsert_item_name(item_id, name)

        insert_median_price(item_id, timestamp, median_price)

    print("data inserted")

if __name__ == "__main__":
    run_once()