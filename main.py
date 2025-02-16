from datetime import datetime
import queries
import sort
import pytz


def convert_epoch(epoch_timestamp: str):
    int_epoch = int(epoch_timestamp)
    timestamp_s = int_epoch / 1000
    utc_dt = datetime.fromtimestamp(timestamp_s, tz=pytz.utc)
    return utc_dt


def pull_item_price(item_id: str):
    """
    Queries Tarkov api for all item price data for an item
    :param item_id: String id of item
    :return: List[Dictionary]
                "price": Sell price of item id
                "timestamp":
    """
    query = queries.pull_item_price_query(item_id)
    try:
        res = queries.run_query(query)
        item_prices = res["data"]["itemPrices"]
        return item_prices
    except Exception as e:
        print(f"Failed to pull item price data.\n{e}")


def get_best_vendor(item_id) -> dict:
    """
    Queries Tarkov api for highest purchase price of an item from a vendor and returns vendor details
    :param item_id: String id of item
    :return: Dictionary:
                "price": Highest value vendor pays in any currency
                "priceRUB": Rubles that vendor pays for item
                "vendor": Dictionary: "name": Vendor's name
    """
    query = queries.pull_vendor_sell_price(item_id)
    try:
        res = queries.run_query(query)
        vendor_data = res["data"]["item"]["sellFor"]
        best_vendor = {
            "price": 0,
            "priceRUB": 0,
            "vendor": {
                "name": "Base"
            }}
        for ven in vendor_data:
            if ven["priceRUB"] > best_vendor["priceRUB"] and ven["vendor"]["name"] != "Flea Market":
                best_vendor = ven
        return best_vendor

    except Exception as e:
        print(f"Failed to pull vendor data.\n{e}")


def check_item_profitability(item: dict):
    # print(f"[*] Checking for best vendor on {item["name"]}...", flush=True)

    # Get best vendor for an item
    vendor = get_best_vendor(item["id"])
    # print(f"[*] Best vendor found: {vendor["vendor"]["name"]}", end="\r", flush=True)

    # Get all prices for an item
    # print(f"[*] Pulling prices for {item["name"]}...", end="\r", flush=True)
    prices = pull_item_price(item["id"])

    # Reduce prices to only items that are profitable to flip
    # print(f"[*] Checking profitability to target vendor...", end="\r", flush=True)
    profitable = []
    price_aggregate = []

    for val in prices:
        if vendor["priceRUB"] - val["price"] > 1000:
            price_aggregate.append(val["price"])
            profitable.append(val)

    if price_aggregate:
        avg_price = int(sum(price_aggregate) / len(price_aggregate))
    else:
        avg_price = 0

    diff = vendor["priceRUB"] - avg_price

    if len(profitable) > 20:
        print(f"{item["name"]:<30}{avg_price:>10}{vendor["priceRUB"]:>10}{vendor["vendor"]["name"]:^15}{diff:^10}")


if __name__ == "__main__":
    # list[Dict: "id", "name", "types"]
    valuables = sort.valuable_items()
    found_flippable = []

    print("Valuables")

    print(f"{'Item':<30}{'Flea':>10}{'VenPays':>10}{'Vendor':^15}{'Delta':^10}")
    print(" ")

    for item in valuables:
        check_item_profitability(item)
