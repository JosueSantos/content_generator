# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from scrapy.exceptions import DropItem
from content_generator.items import MateriaItem

class ContentFile(object):
	def __init__(self):
		self.file = open("content/materias.content", 'w')
		self.arrayId = {
			"jogada_id": "svm.dn.cadernos.jogada.d",
			"jogada": [],
			"seguranca_id": "svm.dn.cadernos.policia.d",
			"seguranca": [],
			"regiao_id": "svm.dn.cadernos.regional.d",
			"regiao": [],
			"pais_id": "svm.dn.cadernos.nacional.d",
			"pais": [],
			"opniao_id": "svm.dn.opinion.d",
			"opniao": [],
			"metro_id": "svm.dn.cadernos.cidade.d",
			"metro": [],
			"mundo_id": "svm.dn.cadernos.internacional.d",
			"mundo": [],
			"negocios_id": "svm.dn.cadernos.negocios.d",
			"negocios": [],
			"politica_id": "svm.dn.cadernos.policia.d",
			"politica": [],
			"verso_id": "svm.dn.cadernos.verso.d",
			"verso": []
		}
		 

	def process_item(self, item, spider):
		self.arrayId[ item.get('editoria') ].append( item.get('id_article') )

		self.file.write("\n")
		self.file.write("## ## ## NEXT ARTICLE\n")
		self.file.write("id:" + item.get('id_article') + "\n")
		self.file.write("major:Article\n")
		self.file.write("\n")

		if ( item.get('image_file') ):
			self.file.write("id:" + item.get('id_image') + "\n")
			self.file.write("major:Article\n")
			self.file.write("inputtemplate:standard.Image\n")
			self.file.write("securityparent:" + item.get('id_article') + "\n")
			self.file.write("file:image.jpg:" + item.get('image_file') + "\n")
			self.file.write('component:contentData:contentData:{"_type"\:"com.atex.standard.image.ImageContentDataBean","title"\:"' + item.get('image_title') + '","caption"\:"' + item.get('image_caption') + '","byline"\:"' + item.get('image_byline') + '"}' + "\n")

		self.file.write("\n")
		self.file.write("id:" + item.get('id_article') + "\n")
		self.file.write("major:Article\n")
		self.file.write("inputtemplate:standard.Article\n")
		self.file.write("securityparent:" + item.get('id_editoria') + "\n")
		self.file.write("name:" + item.get('titulo') + "\n")
		self.file.write("component:byline:value:" + item.get('autor') + "\n")
		self.file.write("component:lead:value:" + item.get('sub_titulo') + "\n")
		self.file.write("component:p.Content.state:onlineState:true\n")
		self.file.write("component:body:value:" + item.get('conteudo') + "\n")
		self.file.write("\n")

		if ( item.get('image_file') ):
			self.file.write("ref:images:0:" + item.get('id_image') + "\n")
			self.file.write("\n")

		return item

	def close_spider(self, spider):
		for key, value in self.arrayId.items():
			if( key == "jogada" ):
				id_editoria = "svm.dn.cadernos.jogada.d"
			elif( key == "seguranca" ):
				id_editoria = "svm.dn.cadernos.policia.d"
			elif( key == "regiao" ):
				id_editoria = "svm.dn.cadernos.regional.d"
			elif( key == "pais" ):
				id_editoria = "svm.dn.cadernos.nacional.d"
			elif( key == "opniao" ):
				id_editoria = "svm.dn.opinion.d"
			elif( key == "metro" ):
				id_editoria = "svm.dn.cadernos.cidade.d"
			elif( key == "mundo" ):
				id_editoria = "svm.dn.cadernos.internacional.d"
			elif( key == "negocios" ):
				id_editoria = "svm.dn.cadernos.negocios.d"
			elif( key == "politica" ):
				id_editoria = "svm.dn.cadernos.policia.d"
			elif( key == "verso" ):
				id_editoria = "svm.dn.cadernos.verso.d"
			else:
				continue

			self.file.write("\n")
			self.file.write("\n")

			self.file.write("id:" + id_editoria + "\n")
			self.file.write("major:Department" + "\n")

			for id_article in value:
				self.file.write("list:resources:" + id_article + "\n")

			self.file.write("\n")
			self.file.write("\n")

		self.file.close()