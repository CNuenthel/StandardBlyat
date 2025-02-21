import requests
import time


def run_query(query, variables=None) -> dict:
    """Runs a GraphQL query asynchronously."""
    url = "https://api.tarkov.dev/graphql"

    if variables:
        json_data = {"query": query, "variables": variables}
    else:
        json_data = {"query": query}

    try:
        res = requests.post(url, json=json_data)
        if res:
            return res.json()
    except Exception as e:
        print(f"Query failed: {e}")
        return None


def pull_item_price_query(item_id: str):
    """
    Builds query to pull price data by a dynamic item id
    :param item_id: String id of target item
    :return: String graphql query
    """
    func = 'itemPrices(gameMode: pve id: "' + item_id + '")'
    fields = """ {
        price
        timestamp
        }
    """
    query = "{" + func + fields + "}"
    return query


def pull_vendor_sell_prices(item_ids: list):
    query = """
    query Items($lang: LanguageCode, $ids: [ID]) {
      items(lang: $lang, ids: $ids) {
        id
        name
        updated
        sellFor {
          vendor {
            name
          }
          priceRUB
        }
      }
    }
    """
    variables = {
        'lang': 'en',
        'ids': item_ids
    }
    return query, variables


def pull_item_price(item_id: str):
    query = pull_item_price_query(item_id)
    res = run_query(query)
    if res:
        prices = res["data"]["itemPrices"]
        return {"id": item_id, "prices": prices}


def sort_prices(time_factor, price_list):
    epoch_now = int(time.time())
    sig_prices = []

    for price in price_list:
        price_timestamp = int(price["timestamp"])/1000
        time_diff = abs(epoch_now - price_timestamp)
        match time_factor:
            case "minute":
                if time_diff <= 300:
                    sig_prices.append(price)
            case "hour":
                if time_diff <= 3600:
                    sig_prices.append(price)
            case "day":
                if time_diff <= 86400:
                    sig_prices.append(price)

    if sig_prices:
        avg_price = sum([item["price"] for item in sig_prices]) / len(sig_prices)
    else:
        avg_price = 0
    return avg_price


if __name__ == "__main__":
    ls = ["60b0f561c4449e4cb624c1d7", "57347baf24597738002c6178"]
    prices = pull_item_price(ls[0])

