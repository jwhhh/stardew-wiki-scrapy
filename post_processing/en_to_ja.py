from processor import StardewItemsProcessor

processor = StardewItemsProcessor()
processor.convert_hiragana()

with open("../out/stardew_items_en_to_ja.csv", "w") as f:
    f.write("# en,ja,hiragana,url,img_url\n")
    for item in processor.items.values():
        f.write(f"{item.en},{item.ja},{item.ja_with_hiragana},{item.url},{item.img_url}\n")
