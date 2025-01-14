import pykakasi


class StardewItem:
    def __init__(self, en, ja, zh, zh_tw, url, img_url):
        self.en = en
        self.ja = ja
        self.zh = zh
        self.zh_tw = zh_tw
        self.url = url
        self.img_url = img_url

    def convert_hiragana(self):
        kks = pykakasi.kakasi()
        result = kks.convert(self.ja)
        self.ja_with_hiragana = ""
        for item in result:
            self.ja_with_hiragana += f"{item['orig']}[{item['hira'].capitalize()}] "
        self.ja_with_hiragana = self.ja_with_hiragana.strip()


class StardewItemsProcessor:
    def __init__(self, filename="../out/stardew_items.csv"):
        self.filename = filename
        self.items = dict()
        self._load()

    def _load(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            items = line.strip().split(",")
            self.items[items[0]] = StardewItem(
                items[0], items[1], items[2], items[3], items[4], items[5]
            )

    def convert_hiragana(self):
        for items in self.items.values():
            items.convert_hiragana()
