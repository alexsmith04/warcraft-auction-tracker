from storage import get_prices_for_item

item_id = input("Item id: ")
data = get_prices_for_item(item_id)
print(data)