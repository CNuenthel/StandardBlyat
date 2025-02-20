from datetime import datetime
from colors import Color, color_text
import queries
import sort
import pyfiglet
import asyncio
import aiohttp
import os
import sys
import time


# def convert_epoch(epoch_timestamp: str):
#     int_epoch = int(epoch_timestamp)
#     timestamp_s = int_epoch / 1000
#     utc_dt = datetime.fromtimestamp(timestamp_s, tz=pytz.utc)
#     return utc_dt
#

# TODO this now pulls all item prices at once
async def pull_item_prices(session, item_ids: list):
    """Queries Tarkov API asynchronously for item price data."""
    item_prices = {}
    for item_id in item_ids:
        query = queries.pull_item_price_query(item_id)
        res = await queries.run_query(session, query)

        if res:
            item_prices[item_id] = res["data"]["itemPrices"]
    return item_prices


async def get_best_vendors(session, item_ids: list):
    """Queries Tarkov API asynchronously for the best vendor price."""
    query, variables = queries.pull_vendor_sell_prices(item_ids)
    res = await queries.run_query(session, query, variables)

    vendors = {}

    if res:
        for item in res["data"]["items"]:
            vendor_data = item["sellFor"]
            best_vendor = {
                "price": 0,
                "priceRUB": 0,
                "vendor": {"name": "Base"}
            }
            for ven in vendor_data:
                if ven["priceRUB"] > best_vendor["priceRUB"] and ven["vendor"]["name"] != "Flea Market":
                    best_vendor = ven
            vendors[item["id"]] = best_vendor


async def check_item_profitability(session, items: list):
    """Checks item profitability asynchronously."""
    print(items)
    # vendor_task = get_best_vendors(session, items)
    # prices_task = pull_item_prices(session, items)
    #
    # vendor, prices = await asyncio.gather(vendor_task, prices_task)
    # print(vendor)
    # print(prices)
    #
    # print(vendor)
    # print(prices)
    #
    # profitable = []
    # price_aggregate = []
    #
    # for val in prices:
    #     if vendor["priceRUB"] - val["price"] > 1000:
    #         price_aggregate.append(val["price"])
    #         profitable.append(val)
    #
    # avg_price = int(sum(price_aggregate) / len(price_aggregate)) if price_aggregate else 0
    # diff = vendor["priceRUB"] - avg_price
    #
    # if len(profitable) > 20:
    #     if diff <= 2000:
    #         print(
    #             color_text(
    #                 f"{item['name']:<35}{avg_price:>10}{vendor['priceRUB']:>10}{vendor['vendor']['name']:^15}{diff:^10}",
    #                 Color.BRTBLUE
    #             )
    #         )
    #     elif 2001 <= diff <= 3000:
    #         print(
    #             color_text(
    #                 f"{item['name']:<35}{avg_price:>10}{vendor['priceRUB']:>10}{vendor['vendor']['name']:^15}{diff:^10}",
    #                 Color.BRTCYAN
    #             )
    #         )
    #     elif diff > 3000:
    #         print(
    #             color_text(
    #                 f"{item['name']:<35}{avg_price:>10}{vendor['priceRUB']:>10}{vendor['vendor']['name']:^15}{diff:^10}",
    #                 Color.BRTGREEN
    #             )
    #         )


def print_table_header():
    print(
        color_text(
            f"{'Item':<35}{'Flea':>10}{'VenPays':>10}{'Vendor':^15}{'Delta':^10}",
            Color.CYAN
        )
    )
    print(" ")


async def main():
    os.system("cls")
    
    banner = pyfiglet.figlet_format("StandardBlyat")
    lists = sort.LISTS
    list_map = {i + 1: k for i, k in enumerate(lists.keys())}
    list_strs = [color_text(f"{k}: {v}", Color.CYAN) for k, v in list_map.items()]
    list_strs.append(color_text("\nType Exit to Quit.", Color.BRTRED))

    async with aiohttp.ClientSession() as session:
        while True:
            print("=" * 68)
            print(banner)
            print("=" * 68)

            try:
                inp = input(f"\n{"\n".join(list_strs)}\n\nPlease select a list to scan: ")

                if inp.lower() == "exit":
                    os.system("cls")
                    print("\n Goodbye!")
                    time.sleep(2)
                    sys.exit()

                inp = int(inp)

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

            print("\n\033[36m15-2, 15-4 That's all there is, there ain't no more.\033[0m")
            input("\033[36mPress Enter to select a new scan list...\033[0m")
            os.system("cls")


if __name__ == "__main__":
    asyncio.run(main())
