import aiohttp
import asyncio
import json


async def run_query(session, query, variables):
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
    query = """
    {
        itemPrices($id: String!, $gameMode: pve) {
            price
            timestamp
        }
    }
    """
    variables = {
        'id': item_id,
        "gameMode": "pve",
    }
    return query, variables


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
