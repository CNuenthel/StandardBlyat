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


if __name__ == "__main__":
    # list[Dict: "id", "name", "types"]
    valuables = sort.valuable_items()
    found_flippable = []
    for item in valuables:
        print(f"[*] Checking for best vendor on {item["name"]}...")
        # Get best vendor for an item
        vendor = get_best_vendor(item["id"])
        print(f"[*] Best vendor found: {vendor["vendor"]["name"]}")

        # Get all prices for an item
        print(f"[*] Pulling prices for {item["name"]}...")
        prices = pull_item_price(item["id"])

        # Reduce prices to only items that are profitable to flip
        print(f"[*] Checking profitability to target vendor...")
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

        if len(profitable) > 20:
            flip_data = {"ven_pays": vendor["priceRUB"], "item_name": item["name"], "avg_flea_price": avg_price, "vendor_name": vendor["vendor"]["name"]}
            found_flippable.append(flip_data)
            print(f"[*] {item["name"]} is profitable, found {len(profitable)} items flippable to {vendor["vendor"]["name"]}")
        else:
            print(f"[*] {item["name"]} is not profitable, moving on...")

    if found_flippable:
        for item in found_flippable:
            print(f"{item["item_name"]}:")
            print(f"    Average flea price: {item["avg_flea_price"]}")
            print(f"    Top vendor: {item["vendor_name"]}")
            print(f"    Vendor offer: {item["ven_pays"]}")
    else:
        print("Yikes... no detected flippable items")
