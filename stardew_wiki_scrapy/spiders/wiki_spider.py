from pathlib import Path

import scrapy


class StardewItem:
    def __init__(self, en, url, img_url):
        self.en = en
        self.ja = None
        self.zh = None
        self.zh_tw = None
        self.url = url
        self.img_url = img_url

    def set_translation(self, translation, lang):
        if lang == "ja":
            self.ja = translation
        elif lang == "zh":
            self.zh = translation
        elif lang == "zh-tw":
            self.zh_tw = translation

    def is_complete(self):
        return all([self.en, self.ja, self.zh, self.zh_tw])

    def __str__(self):
        return f"{self.en},{self.ja},{self.zh},{self.zh_tw}"


class WikiSpider(scrapy.Spider):
    name = "stardew_wiki"
    base_url = "https://stardewvalleywiki.com"
    start_url = "https://stardewvalleywiki.com/Category:Content"
    fallback_img = "https://stardewvalley.net/wp-content/uploads/2017/12/med_logo.png"

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
            img_url = self._get_img_url(response)
            item = StardewItem(stardew_item_en, response.url, img_url)
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
        if lang == "zh":
            yield scrapy.Request(
                self._convert_zh_to_zh_tw(response.url),
                self.parse_zh_tw,
                meta={"stardew_item": item},
            )
        yield from self._save_if_complete(item)

    def parse_zh_tw(self, response):
        stardew_item_zh_tw = response.css(".firstHeading::text").get()
        item = response.meta["stardew_item"]
        item.set_translation(stardew_item_zh_tw, "zh-tw")
        yield from self._save_if_complete(item)
     
    def _get_img_url(self, response):
        img_url = response.css("#infoboxtable img::attr(src)").get()
        if img_url is None:
            img_url = response.css(".thumb.tright img::attr(src)").get()
        if img_url is None:
            return self.fallback_img
        else:
            return f"{self.base_url}{img_url}"
    
    def _convert_zh_to_zh_tw(self, zh):
        base_url = zh.split('.com')[0] + '.com'
        title = zh.split('.com/')[1]
        new_url = f"{base_url}/mediawiki/index.php?title={title}&variant=zh-tw"
        return new_url
    
    def _save_if_complete(self, item):
        if item.is_complete():
            self.log(f"Completed item: {item}")
            yield {
                "en": item.en,
                "ja": item.ja,
                "zh": item.zh,
                "zh-tw": item.zh_tw,
                "url": item.url,
                "img_url": item.img_url,
            }
