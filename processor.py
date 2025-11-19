import json
import statistics
from collections import defaultdict
from fetch import get_item_info_by_id

def normalise_auction(auction):

    buyout_price = auction.get('buyout')
    
    if not buyout_price:
        return None

    else:
        item_id = auction['item']['id']
        quantity = auction['quantity']
        unit_price = buyout_price/quantity

        auction = {'id': item_id, 'quantity': quantity, 'buyout_price': buyout_price, 'unit_price': unit_price}
        return auction

def group_auctions_by_item_id(normalised_auctions):
    
    price_map = defaultdict(list)

    for auction in normalised_auctions:

        if auction is not None:
            price_map[auction['id']].append(auction['unit_price'])

    return price_map

def calculate_median(price_map):
    
    medians = {}

    for item_id, prices in price_map.items():
        median_price = statistics.median(prices)
        medians[item_id] = median_price

    return medians

def compute_item_medians(data):

    normalised_auctions = []
    for auction in data['auctions']:
        normalised_auctions.append(normalise_auction(auction))

    price_map = group_auctions_by_item_id(normalised_auctions)
    medians = calculate_median(price_map)

    return medians

def get_item_name_from_id(item_id):
    item_info = get_item_info_by_id(item_id)
    if item_info is not None:
        item_name = item_info["name"]
        print(item_name)