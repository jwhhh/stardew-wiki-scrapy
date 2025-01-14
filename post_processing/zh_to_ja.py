from processor import StardewItemsProcessor

processor = StardewItemsProcessor()
processor.convert_hiragana()

with open("../out/stardew_items_zh_to_ja.csv", "w") as f:
    f.write("# zh_tw,ja,hiragana,url,img_url\n")
    for item in processor.items.values():
        f.write(f"{item.zh_tw},{item.ja},{item.ja_with_hiragana},{item.url},{item.img_url}\n")
