from selenium import webdriver
from scrapy import Spider
from spider.items import ImageItem

class ImgSpider(Spider):
    """Implementation of the spider that parses response"""
    # Names should be unique in one project
    name = "ImgSpider"
    allowed_domains = [
        "generated.photos"
    ]
    # The urls where the spider begins crawling
    start_urls = [
        "https://generated.photos/faces/"
    ]

    def __init__(self):
        # Initialize selenium that drives Chrome Canary to navigate pages
        self._driver = webdriver.chrome()

    def parse(self, response):
        """Method that defines how we want to parse the response"""
        self._driver.get(self.__class__.start_urls[0])

        while True:
            try:
                btn_next = self._driver.find_element_by_css_selector("button.loadmore-btn")
                if not btn_next:
                    # end of the page
                    pass
                else:
                    btn_next.click()
            except Exception:
                pass

            # TODO: integration of selenium or another way out

        self._driver.close()
        gallery = response.css("div.grid-photos")

    def parse_helper(self, img_src, img_meta):
        """Helper function that parses all data in an <a> tag"""
        img_meta["sex"] = img_src.css("").extract()[0]


