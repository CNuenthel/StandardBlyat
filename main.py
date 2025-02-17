from datetime import datetime
import queries
import sort
import pytz
import asyncio
import aiohttp


# def convert_epoch(epoch_timestamp: str):
#     int_epoch = int(epoch_timestamp)
#     timestamp_s = int_epoch / 1000
#     utc_dt = datetime.fromtimestamp(timestamp_s, tz=pytz.utc)
#     return utc_dt
#

async def pull_item_price(session, item_id: str):
    """Queries Tarkov API asynchronously for item price data."""
    query = queries.pull_item_price_query(item_id)
    res = await queries.run_query(session, query)

    if res:
        return res.get("data", {}).get("itemPrices", [])
    print(f"Failed to pull item price data for {item_id}")
    return []


async def get_best_vendor(session, item_id: str):
    """Queries Tarkov API asynchronously for the best vendor price."""
    query = queries.pull_vendor_sell_price(item_id)
    res = await queries.run_query(session, query)

    if res:
        vendor_data = res.get("data", {}).get("item", {}).get("sellFor", [])
        best_vendor = {
            "price": 0,
            "priceRUB": 0,
            "vendor": {"name": "Base"}
        }
        for ven in vendor_data:
            if ven["priceRUB"] > best_vendor["priceRUB"] and ven["vendor"]["name"] != "Flea Market":
                best_vendor = ven
        return best_vendor


async def check_item_profitability(session, item):
    """Checks item profitability asynchronously."""
    vendor_task = get_best_vendor(session, item["id"])
    prices_task = pull_item_price(session, item["id"])

    vendor, prices = await asyncio.gather(vendor_task, prices_task)

    profitable = []
    price_aggregate = []

    for val in prices:
        if vendor["priceRUB"] - val["price"] > 1000:
            price_aggregate.append(val["price"])
            profitable.append(val)

    avg_price = int(sum(price_aggregate) / len(price_aggregate)) if price_aggregate else 0
    diff = vendor["priceRUB"] - avg_price

    if len(profitable) > 20:
        print(f"{item['name']:<35}{avg_price:>10}{vendor['priceRUB']:>10}{vendor['vendor']['name']:^15}{diff:^10}")


def print_table_header():
    print(f"{'Item':<35}{'Flea':>10}{'VenPays':>10}{'Vendor':^15}{'Delta':^10}")
    print(" ")


async def main():
    lists = sort.LISTS
    list_map = {i + 1: k for i, k in enumerate(lists.keys())}
    list_strs = [f"{k}: {v}" for k, v in list_map.items()]

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                inp = int(input(f"\nPlease select a list to scan...\n{"\n".join(list_strs)}\n"))
                if inp not in list_map:
                    print("Invalid selection. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            scan_list = lists[list_map[inp]]

            print(f"\nScanning {list_map[inp]}...\n")
            print_table_header()

            tasks = [check_item_profitability(session, item) for item in scan_list]
            await asyncio.gather(*tasks)

            print("\n15-2, 15-4 That's all there is, there ain't no more.")


if __name__ == "__main__":
    asyncio.run(main())
