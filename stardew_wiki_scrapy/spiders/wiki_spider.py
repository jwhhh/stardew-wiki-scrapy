from pathlib import Path

import scrapy


class StardewItem:
    def __init__(self, english, chinese=None, japanese=None):
        self.english = english
        self.chinese = chinese
        self.japanese = japanese

    def set_translation(self, translation, lang):
        if lang == "zh":
            self.chinese = translation
        elif lang == "ja":
            self.japanese = translation

    def is_complete(self):
        return self.chinese is not None and self.japanese is not None

    def __str__(self):
        return f"{self.english}, {self.chinese} {self.japanese}"


class WikiSpider(scrapy.Spider):
    name = "stardew_wiki"
    base_url = "https://stardewvalleywiki.com"
    start_url = "https://stardewvalleywiki.com/Category:Content"

    def start_requests(self):
        self.stardew_items = dict()
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        self.log(f"Processing page: {page}")
        if "Category:" in page:
            yield from self._process_category(response)
        else:
            yield from self._process_english_page(response)

    def _process_category(self, response):
        for link in response.css(".mw-category a::attr(href)").getall():
            new_url = f"{self.base_url}{link}"
            self.log(f"Found link {new_url}")
            yield scrapy.Request(new_url, self.parse)

    def _process_english_page(self, response):
        stardew_item_en = response.css(".firstHeading::text").get()
        if stardew_item_en not in self.stardew_items:
            item = StardewItem(stardew_item_en)
            for lang in ["zh", "ja"]:
                translation = response.css(
                    f".interlanguage-link.interwiki-{lang} a::attr(href)"
                ).get()
                if translation:
                    yield scrapy.Request(
                        translation, self.parse_translation, meta={"stardew_item": item}
                    )

    def parse_translation(self, response):
        lang = "zh" if "zh" in response.url else "ja"
        stardew_item_trans = response.css(".firstHeading::text").get()
        item = response.meta["stardew_item"]
        item.set_translation(stardew_item_trans, lang)
        if item.is_complete():
            self.log(f"Completed item: {item}")
            yield {
                "english": item.english,
                "chinese": item.chinese,
                "japanese": item.japanese,
            }
