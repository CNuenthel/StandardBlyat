import requests

URL = "https://api.tarkov.dev/graphql"


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post(URL, headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def pull_items_query():
    """
    Builds query to pull all item data and display fields: id, name, types
    :return: String graphql query
    """
    query = """
    {
        items(lang: en) {
            id
            name
            types
            }
    }
    """
    return query


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


def pull_vendor_sell_price(item_id: str):
    func = 'item(gameMode: pve id: "' + item_id + '")'
    fields = """ {
        id
        name
        sellFor {
            price
            priceRUB
            vendor {
                name
            }
        }
    }
    """
    query = "{" + func + fields + "}"
    return query


if __name__ == "__main__":
    res = run_query(pull_vendor_sell_price("57347b8b24597737dd42e192"))
