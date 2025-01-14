from processor import StardewItemsProcessor

processor = StardewItemsProcessor()
processor.convert_pinyin()

with open("../out/stardew_items_en_to_zh.csv", "w") as f:
    f.write("# en,zh_tw,pinyin,url,img_url\n")
    for item in processor.items.values():
        f.write(
            f"{item.en},{item.zh_tw},{item.zh_with_pinyin},{item.url},{item.img_url}\n"
        )
