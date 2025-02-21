import sqlite3
import json


class ItemsDB:
    def __init__(self, items_dict_path="item_lists/primary_list.json", db_path="db/items.db"):
        self.db_path = db_path
        self.items_dict_path = items_dict_path

        self._create_item_table()

    def _create_item_table(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                types TEXT NOT NULL,
                vendor TEXT,
                sell_for INTEGER,
                flea_avg_price INTEGER,
                delta INTEGER 
            )
            """
                         )
        conn.commit()
        conn.close()

    def insert_items(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        with open(self.items_dict_path, "r") as f:
            items = json.load(f)
        for item in items:
            cur.execute(
                """INSERT INTO items (id, name, types, vendor, sell_for, flea_avg_price, delta) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (item["id"], item["name"], json.dumps(item["types"]), "Base", 0, 0, 0)
            )
        conn.commit()
        conn.close()

    def update_item_vendor_data(self, item_data: list):
        """
        Item data needs to be passed as a list of dictionaries
        { 'vendor': 'vendor_name', 'priceRUB': 99999, 'id': 5483249823948}
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        for item in item_data:
            cur.execute(
                "UPDATE items SET vendor = ?, sell_for = ? WHERE id = ?",
                (item["vendor"], item["priceRUB"], item["id"])
            )
        conn.commit()
        conn.close()

    def update_item_flea_data(self, item_data: list):
        """
        Item data needs to be passed as a list of dictionaries
        { 'flea_avg_price': 1234123, 'delta': 1234, 'id': 5483249823948}
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        for item in item_data:
            cur.execute(
                "UPDATE items SET flea_avg_price = ?, delta = ? WHERE id = ?",
                (item["flea_avg_price"], item["delta"], item["id"])
            )
        conn.close()

    def fetch_item_data_by_id(self, item_ids: list):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        placeholders = ",".join("?" * len(item_ids))
        query = f"SELECT * FROM items WHERE id IN ({placeholders})"

        cur.execute(query, item_ids)
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "id": row[0],
                "name": row[1],
                "types": json.loads(row[2]),
                "vendor": row[3],
                "sell_for": row[4],
                "flea_avg_price": row[5],
                "delta": row[6]
            }
            for row in rows
        ]

    def fetch_all_item_ids(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        query = "SELECT id FROM items"
        cur.execute(query)
        ids = [row[0] for row in cur.fetchall()]
        conn.close()
        return ids





