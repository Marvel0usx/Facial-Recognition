# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import Request
from itemadapter import ItemAdapter
from spider.items import ImageItem
from scrapy.exceptions import DropItem


class MongoDBPipeline:
    """Cutomized pipeline that stores data to a MongoDB instance."""
    collection_name = "faceData"

    def __init__(self, mongo_uri, mongo_db_name):
        """Initialize connection to local MongoDB"""
        self.mongo_uri = mongo_uri
        self.mongo_db_name = mongo_db_name

    @classmethod
    def from_crawler(cls, crawler):
        """This method is called to initialize new pipeline."""
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db_name=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client.get_database(self.mongo_db_name)
        self.collection = self.db.get_collection(self.__class__.collection_name)

    def process_item(self, item: ImageItem, spider):
        """This method is called for every item pipeline component."""
        image_meta = ItemAdapter(item).asdict()
        self.collection.insert_one(image_meta)
        if not item.image_src:
            raise DropItem("Missing image url.")
        # Method must either return an item, raise DropItem, or return Deferred
        else:
            return item

    def close_spider(self, spider):
        self.client.close()
