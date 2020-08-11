from scrapy import Spider
from scrapy_splash import SplashRequest
from spider.items import ImageItem


class ImageSpider(Spider):
    """Implementation of the spider that parses response"""
    # Names should be unique in one project
    name = "ImageSpider"
    allowed_domains = [
        "generated.photos"
    ]
    # The urls where the spider begins crawling
    start_urls = [
        "https://generated.photos/faces/"
    ]

    def __init__(self):
        self.timeout = 0.5
        self.last_visit_info = None
        self.num_to_go = 50000
        self.btn_click = "document.querySelector('button.loadmore-button').click()"

    def start_requests(self):
        new_header = self.shuffle_request_header()
        while self.num_to_go > 0:
            self.num_to_go -= 1
            yield SplashRequest(
                url=self.__class__.start_urls[0],
                callback=self.parse,
                endpoint="render.json",
                args={
                    'wait': self.timeout,
                    'js_source': self.btn_click,
                },
                splash_headers=ImageSpider.shuffle_request_header()
            )

    def parse(self, response):
        """Method that defines how we want to parse the response"""
        # Obtain tags
        if response:
            print(f"!!!!!!!!!!!!!{response}!!!!!!!!!!!!!")

    @staticmethod
    def shuffle_request_header():
        return {}