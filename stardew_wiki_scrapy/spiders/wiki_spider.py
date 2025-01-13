from pathlib import Path

import scrapy


class WikiSpider(scrapy.Spider):
    name = "stardew_wiki"
    base_url = "https://stardewvalleywiki.com"
    start_url = "https://stardewvalleywiki.com/Category:Content"

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        if page.startswith("Category:"):
            self.log(f"Crawled page {page}")
            for link in response.css(".mw-category a::attr(href)").getall():
                new_url = f"{self.base_url}{link}"
                self.log(f"Found link {new_url}")
                yield scrapy.Request(new_url, self.parse)
        else:
            pass  # TODO
