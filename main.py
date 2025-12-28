import queries
import asyncio
import aiohttp
import os
import sys
import time
import json

from pathlib import Path
from colors import Color, color_text


class VendorDataException(Exception):
    def __init__(self, prop_exception):
        super().__init__(f"Failed to pull Vendor Data.\n{prop_exception}")


def load_list_components():
    lists = {}
    item_list_directory = Path("item_lists")
    for p in item_list_directory.iterdir():
        with open(p, "r") as f:
            lists[" ".join(p.name.split(".")[0].split("_")).title()] = json.load(f)
    return lists


async def pull_item_price(session, item_id: str):
    """Queries Tarkov API asynchronously for item price data."""
    query = queries.pull_item_price_query(item_id)
    try:
        res = await queries.run_query(session, query)
        return res.get("data", {}).get("itemPrices", [])
    except Exception as e:
        return []


async def get_best_vendor(session, item_ids: list):
    """ Queries Tarkov API for vendor data and builds a lookup table of best sale vendors for each listed item. """
    query, variables = queries.pull_vendor_sell_prices(item_ids)

    try:
        res = await queries.run_query(session, query)
        item_data = {}
        items = res["data"]["items"]

        for item in items:
            vendors = item["sellFor"]
            best_vendor, best_price = {"priceRUB": 0, "vendor": {"name": "None"}}, 0

            for vendor in vendors:
                if vendor["priceRUB"] > best_price and vendor["vendor"]["name"] != "Flea Market":
                    best_vendor = vendor
                    best_price = vendor["priceRUB"]

            data = {
                "vendor": best_vendor["vendor"]["name"],
                "priceRUB": best_vendor["priceRUB"],
                "id": item["id"]
            }

            item_data[item["id"]] = data

        return item_data
    except Exception as e:
        raise VendorDataException(e)

async def check_item_profitability(session, item, vend: dict, time_factor: str):
    time_windows = {
        "minute": 300,
        "hour": 3600,
        "day": 86400,
        "all_time": float("inf"),
    }

    try:
        max_age = time_windows[time_factor]
    except KeyError:
        raise ValueError(
            "Improper time factor passed to function.\n"
            "Acceptable time factors: 'minute', 'hour', 'day', 'all_time'"
        )

    prices = await pull_item_price(session, item["id"])

    now = int(time.time())
    profitable = []

    for val in prices:
        price_diff = vend["priceRUB"] - val["price"]
        if price_diff <= 1000:
            continue

        age = abs(now - (int(val["timestamp"]) // 1000))
        if age <= max_age:
            profitable.append(val)

    if len(profitable) <= 5:
        return

    avg_price = int(sum(v["price"] for v in profitable) / len(profitable))
    diff = vend["priceRUB"] - avg_price

    color_thresholds = [
        (3000, Color.BRTGREEN),
        (2000, Color.BRTCYAN),
        (0, Color.BRTBLUE),
    ]

    color = next(c for threshold, c in color_thresholds if diff >= threshold)

    print(
        color_text(
            f"{item['name']:<50}"
            f"{avg_price:>10}"
            f"{vend['priceRUB']:>10}"
            f"{vend['vendor']:^15}"
            f"{diff:^10}",
            color,
        )
    )


def print_table_header():
    print(
        color_text(
            f"{'Item':<50}{'Flea':>10}{'VenPays':>10}{'Vendor':^15}{'Delta':^10}",
            Color.CYAN
        )
    )
    print(" ")


async def main():
    banner = r"""
 _____         _           ____                  
|_   _|___ ___| |_ ___ _ _|    \ ___ ___ ___ ___ 
  | | | .'|  _| '_| . | | |  |  |  _| . |   | -_|
  |_| |__,|_| |_,_|___|\_/|____/|_| |___|_|_|___|  
    """

    os.system("cls")

    lists = load_list_components()
    list_map = {i + 1: k for i, k in enumerate(lists.keys())}
    list_strs = [color_text(f"{k}: {v}", Color.CYAN) for k, v in list_map.items()]
    list_strs.append(color_text("\nType Exit to Quit.", Color.BRTRED))

    print(color_text("Pulling vendor information...", Color.BRTCYAN))

    async with aiohttp.ClientSession() as session:
        try:
            vendors = await get_best_vendor(session, [item["id"] for item in lists["Primary List"]])
        except VendorDataException as e:
            print(color_text("Failed to parse vendor data. Exiting.", Color.BRTRED))
            print("")
            print(e)
            return

        ven_flag = False
        ven_show = False

        print(color_text("Done.", Color.BRTGREEN))
        print(banner)

        while True:
            try:
                time_map = {1: "minute", 2: "hour", 3: "day", 4: "all_time"}
                time_fac_input = int(
                    input(
                        f"\n"
                        f"1. Minute\n"
                        f"2. Hour\n"
                        f"3. Day\n"
                        f"4. All Time\n"
                        f"\n"
                        f"\n"
                        f"Please select a time factor to limit flea market data.\n"
                        f"The time factor will define how far back flea market data\n"
                        f"will be reviewed for items.\nTime Factor (1-4): "
                    )
                )

                if time_fac_input not in [1, 2, 3, 4]:
                    print("Invalid selection. Try again.")
                    continue

                time_factor = time_map[time_fac_input]
                os.system("cls")
                break

            except ValueError:
                input("Invalid input. Press Enter to Continue.")
                continue

        while True:
            try:
                inp = input(f"\n{"\n".join(list_strs)}\n\nVen: {ven_show}\n\nPlease select a list to scan: ")

                if inp.lower() == "exit":
                    os.system("cls")
                    print("\n Goodbye!")
                    time.sleep(2)
                    sys.exit()

                if inp.lower() == "ven":
                    ven_show = not ven_show
                    continue

                if inp.isdigit():
                    inp = int(inp)

                if inp not in list_map:
                    input("Invalid selection. Try again. Press Enter to Continue")
                    continue

            except ValueError:
                input("Invalid input. Press enter to continue.")
                continue

            if not vendors:
                if ven_flag:
                    print("Unable to pull vendor data, сука блять...")
                    time.sleep(3)
                    sys.exit()

                print("Vendor query failed, attempting new vendor scan...")
                vendors = await get_best_vendor(session, [item["id"] for item in lists["Primary List"]])
                ven_flag = True

            scan_list = lists[list_map[inp]]

            if ven_show:
                ls = [color_text(
                            f"{item['name']:<50}"
                            f"{vendors[item["id"]]["vendor"]:>10}"
                            f"{vendors[item["id"]]["priceRUB"]:^15}",
                            Color.BRTBLUE
                        ) for item in scan_list]
                sorted_ls = sorted(ls)
                for item in sorted_ls:
                    print(item)

            else:
                print(f"\nScanning {list_map[inp]}...\n")
                start = time.time()
                print_table_header()

                tasks = [check_item_profitability(session, item, vendors[item["id"]], time_factor) for item in
                         scan_list]
                await asyncio.gather(*tasks)

            end = time.time()
            print("\n" + color_text(f"List scan completed in {end-start:.3f} seconds.", Color.CYAN))
            input(color_text("Press Enter to select a new scan list...", Color.CYAN))
            os.system("cls")


if __name__ == "__main__":
    asyncio.run(main())
