

async def run_query(session, query, variables=None):
    """Runs a GraphQL query asynchronously."""
    url = "https://api.tarkov.dev/graphql"
    try:
        async with session.post(url, json={"query": query, "variables": variables}) as response:
            return await response.json()
    except Exception as e:
        print(f"Query failed: {e}")
        return None


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

