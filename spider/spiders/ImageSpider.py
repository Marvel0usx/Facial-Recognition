from scrapy import Spider
from scrapy_splash import SplashRequest
from spider.items import ImageItem
from bs4 import BeautifulSoup
import re

class ImageSpider(Spider):
    """Implementation of the spider that parses response"""
    # Names should be unique in one project
    name = "ImageSpider"
    allowed_domains = [
        "generated.photos"
    ]
    # The urls where the spider begins crawling
    start_urls = [
        # "https://httpbin.org/get",
        "https://generated.photos/faces/"
    ]

    def __init__(self):
        self.timeout = 0.5
        self.last_visit_info = None
        self.num_to_go = 50000
        # self.btn_click = "document.querySelector('button.loadmore-button').click()"

    def start_requests(self):
        new_header = self.shuffle_request_header()
        while self.num_to_go > 0:
            yield SplashRequest(
                url=self.__class__.start_urls[0],
                callback=self.parse,
                endpoint="render.html",
                args={
                    'wait': self.timeout,
                },
                headers=ImageSpider.shuffle_request_header()
            )

    def parse(self, response):
        """Method that defines how we want to parse the response"""
        # Obtain tags
        if response.status == 200:
            soup = BeautifulSoup(response._body, 'lxml')
            image_links = soup.select("div.card-image > a[href]")
            for link in image_links:
                description = link["href"]
                src = link.select_one("img")['src']
                print(f"Getting image description: {description} via {src}")
                yield self.encap(description, src)
        else:
            print(f"[Error] Response of code {response.status}")

    def encap(self, description, src):
        new_item = ImageItem()
        new_item["image_src"] = src
        self.parse_labels(new_item, description)
        return new_item

    def parse_labels(self, new_item, description):
        # new_item["sex"], new_item["age"], new_item["ethnicity"], \
        # new_item["emotion"], new_item["hair_color"], new_item["eye_color"]
        labels = description[6:].split("-")
        for label in labels:
            # TODO(harry): finish label parsing
            pass

    @staticmethod
    def shuffle_request_header():
        return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36", }