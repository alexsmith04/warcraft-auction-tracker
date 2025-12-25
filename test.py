import json
import statistics
from collections import defaultdict
from fetch import get_item_info_by_id, get_commodities
from storage import get_market_overview

def get_market_overview_hahah():
    rows = get_market_overview()
    print(rows)
    return rows

get_market_overview_hahah()