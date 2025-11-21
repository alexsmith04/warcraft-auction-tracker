from storage import get_prices_for_item
from processor import get_item_name_from_id, convert_price

item_id = input("Item id: ")
data = get_prices_for_item(item_id)
name = get_item_name_from_id(item_id)
price = convert_price(data[0][1])
print(f"{name} : {data}")