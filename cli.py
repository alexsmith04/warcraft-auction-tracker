from storage import get_prices_for_item, get_item_id_from_name
from processor import get_item_name_from_id, convert_price
from graphing import create_price_history

#name = input("Item name: ")
#item_id = get_item_id_from_name(name)[0][0] #returns a list with a tuple, item id is first item
data = create_price_history()
#price = convert_price(data[0][1])
#print(f"{name} : {data}")