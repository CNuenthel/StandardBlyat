import json

with open("items.json", "r") as f:
    ITEMS = json.load(f).get("items")


def valuable_items():
    val_items = [
        "Antique teapot",
        "Antique vase",
        "Axel parrot figurine",
        "BEAR operative figurine",
        "Battered antique book",
        "Bronze lion figurine",
        "Cat figurine",
        "Chain with Prokill medallion",
        "Chainlet",
        "Cultist figurine",
        "Ded Moroz figurine",
        "Den figurine",
        "Gold skull ring",
        "Golden egg",
        "Golden neck chain",
        "Golden rooster figurine",
        "Horse figurine",
        "Killa figurine",
        "Loot Lord plushie",
        "Old firesteel",
        "Politician Mutkevich figurine",
        "Raven figurine",
        "Reshala figurine",
        "Roler Submariner gold wrist watch",
        "Ryzhy figurine",
        "Scav figurine",
        "Silver Badge",
        "Tagilla figurine",
        "Tamatthi kunai knife replica",
        "USEC operative figurine",
        "Veritas guitar pick",
        "Viibiin sneaker",
        "Wooden clock"
    ]
    matching_items = [item for item in ITEMS if item["name"] in val_items]
    return matching_items


if __name__ == "__main__":
    res = valuable_items()
