# queries.py

class RateLimitError(Exception):
    def __init__(self, retry_after=None):
        self.retry_after = retry_after
        super().__init__("API rate limit hit (429)")


async def run_query(session, query, variables=None):
    url = "https://api.tarkov.dev/graphql"

    async with session.post(
        url, json={"query": query, "variables": variables}
    ) as response:

        if response.status == 429:
            raise RateLimitError(response.headers.get("Retry-After"))

        response.raise_for_status()
        return await response.json()


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


# if __name__ == "__main__":
#     import asyncio
#     import aiohttp
#
#     async def main():
#         async with aiohttp.ClientSession() as session:
#             result = await run_query(session, pull_items_query())
#             return result
#
#     res = asyncio.run(main())