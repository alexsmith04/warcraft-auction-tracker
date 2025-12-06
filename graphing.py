import matplotlib.pyplot as plt
import numpy as np
from storage import get_prices_for_item
from processor import convert_timestamp


def create_price_history():
    item_id = 2770
    data = get_prices_for_item(item_id)

    timestamps = []
    prices = []

    for timestamp, price in data:
        timestamp = convert_timestamp(timestamp)
        timestamps.append(timestamp)
        prices.append(price)

    xpoints = np.array(timestamps)
    ypoints = np.array(prices)

    plt.plot(xpoints, ypoints)
    plt.show()

    return data