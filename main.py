import pysql
import queries
import threading
import time

def pull_vendor_data_thread(db: pysql.ItemsDB):
    ids = db.fetch_all_item_ids()
    query, variables = queries.pull_vendor_sell_prices(ids)
    res = queries.run_query(query, variables)

    if res:
        item_data = []
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
            item_data.append(data)
        db.update_item_vendor_data(item_data)
        print("Vendor Thread Complete")
    else:
        print("Vendor Data Query Failed")


def pull_flea_price_thread(db: pysql.ItemsDB, ids: list, time_factor: str):
    # Time Factor: "minute" | "hour" | "day"
    while True:
        for id in ids:
            prices = queries.pull_item_price(id)
            avg_price = queries.sort_prices(time_factor, prices["prices"])

            db_item = db.fetch_item_data_by_id([id])[0]
            delta = db_item["sell_for"] - avg_price
            item_data = {"flea_avg_price": avg_price, "id": id, "delta": delta}
            db.update_item_flea_data([item_data])
            if delta > 0:
                print(f"{db_item["name"]} | {item_data["delta"]} | {db_item["sell_for"]}")
            time.sleep(1)


if __name__ == "__main__":
    # Build the SQL Table
    db = pysql.ItemsDB()

    if not db.fetch_all_item_ids():
        db.insert_items()

    # Pull updated vendor data
    vendor_thread = threading.Thread(target=pull_vendor_data_thread, args=(db,), daemon=True)
    vendor_thread.start()

    # Cycle item data by one API call a second
    ids = db.fetch_all_item_ids()
    flea_data_thread = threading.Thread(target=pull_flea_price_thread, args=(db, ids, "minute"))
    flea_data_thread.start()
