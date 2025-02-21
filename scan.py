import queries
import pysql

def pull_item_price(item_id: str):
    query = queries.pull_item_price_query(item_id)
    res = queries.run_query(query)
    if res:
        return
        prices = res["data"]["itemPrices"]
        for price in prices



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

def update_prices_thread(database, item_data)
    while True:

if __name__ == "__main__":
    db = pysql.ItemsDB()

    while
    ls = ["5447ac644bdc2d6c208b4567", "5448ba0b4bdc2d02308b456c"]
    res = pull_item_prices(ls)
