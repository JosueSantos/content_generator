# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MateriaItem(scrapy.Item):
	link = scrapy.Field()
	editoria = scrapy.Field()

	id_article = scrapy.Field()
	
	id_image = scrapy.Field()
	image_name = scrapy.Field()
	image_title = scrapy.Field()
	image_caption = scrapy.Field()
	image_byline = scrapy.Field()
	image_file = scrapy.Field()
	
	id_editoria = scrapy.Field()
	titulo = scrapy.Field()
	autor = scrapy.Field()
	sub_titulo = scrapy.Field()
	conteudo = scrapy.Field()