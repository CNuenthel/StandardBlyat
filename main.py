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
        print(f"{item["name"]:<35}{avg_price:>10}{vendor["priceRUB"]:>10}{vendor["vendor"]["name"]:^15}{diff:^10}")


def print_table_header():
    print(f"{'Item':<35}{'Flea':>10}{'VenPays':>10}{'Vendor':^15}{'Delta':^10}")
    print(" ")


if __name__ == "__main__":
    lists = sort.LISTS
    list_map = {i + 1: k for i, k in enumerate(lists.keys())}
    list_strs = [f"{k}: {v}" for k, v in list_map.items()]

    while True:
        try:
            inp = int(input(f"\nPlease select a list to scan...\n{"\n".join(list_strs)}\n"))
        except ValueError:
            continue

        scan_list = lists[list_map[inp]]

        print(f"Scanning {list_map[inp]}\n")
        print_table_header()

        for item in scan_list:
            check_item_profitability(item)

        print("15-2, 15-4 That's all there is, their ain't no more.")




