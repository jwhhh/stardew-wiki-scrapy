from processor import StardewItemsProcessor

processor = StardewItemsProcessor()

with open("../out/stardew_items_zh_to_en.csv", "w") as f:
    f.write("# zh_tw,en,url,img_url\n")
    for item in processor.items.values():
        f.write(f"{item.zh_tw},{item.en},{item.url},{item.img_url}\n")
