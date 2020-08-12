from scrapy import Spider, Request
from scrapy_splash import SplashRequest
from spider.items import ImageItem
from bs4 import BeautifulSoup
import re

ETHNICITY = ["white", "latino", "asian", "black"]
AGE_PREFIX = ["young", "middle"]
AGE = ["adult", "child", "infant"]
EYE_COLOR = ["brown", "grey", "blue", "green"]
HAIR_COLOR = ["brown", "black", "blond", "gray"]
EMOTION = ["joyfull", "neutral"]    # beware of this typo


class ImageSpider(Spider):
    """Implementation of the spider that parses response"""
    name = "ImageSpider"    # Unique identifier
    allowed_domains = ["generated.photos"]
    start_urls = ["https://generated.photos/faces/"]

    def __init__(self):
        self.timeout = 0.5
        self.last_visit_info = None
        self.btn_click = "document.querySelector('button.loadmore-button').click()"

    def start_requests(self):
        """Method that the Scrapy engine calls to dispatch http requests"""
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
        if response.status != 200:
            print(f"[Error] Response of code {response.status}")
        else:
            soup = BeautifulSoup(response.body, 'lxml')
            image_links = soup.select("div.card-image > a[href]")
            for link in image_links:
                description = link["href"]
                src = link.select_one("img")['src']
                if re.match(r"^(http|https)://.*\.jpg$", src):
                    print(f"Getting image description: {description} via {src}", end="\n")
                    yield self.encapsulate(description, src)

            # If the button for loading is found, yield another request with the button clicked

    def encapsulate(self, description, src):
        """Method that factor out all labels from the src and encapsulate to a Scrapy item"""
        new_item = ImageItem()
        labels = description[6:].split("-")
        for label in labels:
            if label in ETHNICITY:
                new_item["ethnicity"] = label
            elif label in EYE_COLOR:
                new_item["eye_color"] = label
            elif label in HAIR_COLOR:
                new_item["hair_color"] = label
            elif label in EMOTION:
                new_item["emotion"] = label[:-1] if label == "joyfull" else label
            if label == "young":
                new_item["age"] = "young-adult"
            elif label == "middle":
                new_item["age"] = "middle-aged"
            if "age" not in new_item and label in AGE:
                new_item["age"] = label
        new_item["image_urls"] = [src]
        return new_item

    @staticmethod
    def shuffle_request_header():
        return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36", }