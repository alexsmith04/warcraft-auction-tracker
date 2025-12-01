from datetime import datetime
from fetch import get_auctions_for_realm
from processor import compute_item_medians, get_item_name_from_id
from storage import init_db, insert_median_price, get_item_name_from_db, upsert_item_name

def run_once():
    init_db()
    print("database initalised")

    data = get_auctions_for_realm()
    print("got data")

    medians = compute_item_medians(data)
    print("medians calculated")

    timestamp = datetime.utcnow().isoformat()
    for item_id, median_price in medians.items():

        name = get_item_name_from_db(item_id)

        if not name:
            name = get_item_name_from_id(item_id)
            if name:
                upsert_item_name(item_id, name)

    insert_median_price(item_id, timestamp, median_price)


if __name__ == "__main__":
    run_once()