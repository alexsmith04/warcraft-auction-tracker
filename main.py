from datetime import datetime
from fetch import get_auctions_for_realm
from processor import compute_item_medians
from storage import init_db, insert_median_price

def main():
    init_db()
    print("database initalised")

    data = get_auctions_for_realm()
    print("got data")

    medians = compute_item_medians(data)
    print("medians calculated")

    timestamp = datetime.utcnow().isoformat()
    for item_id, median_price in medians.items():
        insert_median_price(item_id, timestamp, median_price)
    print("data inserted")

if __name__ == "__main__":
    main()