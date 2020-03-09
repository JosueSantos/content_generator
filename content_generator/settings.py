# -*- coding: utf-8 -*-

# Scrapy settings for content_generator project

BOT_NAME = 'content_generator'

SPIDER_MODULES = ['content_generator.spiders']
NEWSPIDER_MODULE = 'content_generator.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'content_generator.pipelines.ContentFile': 300,
    # 'content_generator.pipelines.SpiderWebCSV': 500,
    'content_generator.pipelines.SpiderWebMongo': 700,
}