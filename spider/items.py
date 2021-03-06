# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ImageItem(Item):
    """This class models the image elements in the response"""

    # Fields of data that we want to obtain and they follow the
    # pattern in the url /joyfull-white-young-adult-male-with-short-brown-hair-and-brown-eyes
    image_urls = Field()    # Required by ImagePipeline
    images = Field()        # Required by ImagePipeline for meta data
    image_id = Field()
    gender = Field()
    age = Field()
    ethnicity = Field()
    emotion = Field()
    hair_color = Field()
    hair_length = Field()
    eye_color = Field()
    confidence = Field()
