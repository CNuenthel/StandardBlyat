import json
import os

LISTS = {}


def format_filename(filename: str):
    """
    Splits a filename string into components and formats a proper name from snake case filenames
    :param filename: String filename
    :return: Dict:
        "raw": The full filename,
        "base_name": filename without extension,
        "proper_name": formatted human-readable filename in title case,
        "file_ext": filename extension only
    """
    components = {
        "raw": filename,
        "base_name": filename.split(".")[0],
        "proper_name": " ".join(filename.split(".")[0].split("_")).title(),
        "file_ext": filename.split(".")[1]

    }
    return components


for filename in os.listdir("item_lists"):
    with open(f"item_lists/{filename}", "r") as f:
        LISTS[format_filename(filename)["proper_name"]] = json.load(f)




# LIST BUILDING BS
#
# with open("item_lists/items.json", "r") as f:
#     ITEMS = json.load(f)
#
# 
# x = [item for item in ITEMS if "provisions" in item["types"]]
#
# with open("item_lists/1.json", "w") as f:
#     json.dump(x, f, indent=2)
