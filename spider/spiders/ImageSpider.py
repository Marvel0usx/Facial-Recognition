from scrapy import Spider, Request
from scrapy.responsetypes import Response
from spider.items import ImageItem
from time import sleep
from json import loads


class ImageSpider(Spider):
    """Implementation of the spider that parses response"""
    name = "ImageSpider"    # Unique identifier
    allowed_domains = ["generated.photos"]

    def start_requests(self):
        """Method that the Scrapy engine calls to dispatch http requests"""
        total_page = self.settings.get("TOTAL_PAGE")
        per_page = self.settings.get("PER_PAGE")

        for page in range(1, total_page + 1):
            yield Request(
                url=self.settings.get("URL").format(page, per_page),
                callback=self.parse,
                method="GET",
                headers=self.settings.get("HEADERS")
            )
            # sleep(10)

    def parse(self, response: Response, **kwargs):
        """Method that defines how we want to parse the response"""
        if response.status != 200:
            print(f"[Error] Response of code {response.status}")
        else:
            json_raw = loads(response.text)
            images = json_raw["images"]
            for image in images:
                new_item = ImageItem()
                new_item["image_id"] = image["id"]
                new_item["image_urls"] = [image["transparent"]["thumb_url"]]
                for key, value in image["meta"].items():
                    new_item[key] = value
                # map(lambda key: new_item.__setitem__(key, image["meta"][key][0]), image["meta"].keys())
                yield new_item
                sleep(0.05)