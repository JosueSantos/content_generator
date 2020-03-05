# -*- coding: utf-8 -*-

import scrapy
import requests

from unidecode import unidecode
from content_generator.items import MateriaItem

class DiarioNordesteSpider(scrapy.Spider):
	name = 'diario_nordeste'
	allowed_domains = ['diariodonordeste.verdesmares.com.br']
	start_urls = [
		# 'https://diariodonordeste.verdesmares.com.br/servicos/ultima-hora',
	]

	def __init__(self, *args, **kwargs):
		try:
			urls = open('urls.csv').readlines()

			for i in range(len(urls)):
				if i != 0:
					url = str(urls[i].strip())
					if( len(url) > 10 ):
						self.start_urls.append(url)

		except FileNotFoundError:
			print('File does not exist')

		self.logger.info(self.start_urls)
		super(DiarioNordesteSpider, self).__init__(*args, **kwargs)

	def parse(self, response):
		if response.css("h1.c-page-head__name a::text").extract_first() == 'Última Hora':
			for article in response.css("article.c-teaser"):
				link = article.css("main.c-teaser__inner div a::attr(href)").extract_first()
				yield response.follow(link, self.parseMateria)

			next_page = response.css("div.c-pagination__next a::attr(href)").extract_first()
			if next_page is not None:
				yield response.follow(next_page, self.parse)
		else:
			link = response.url
			yield response.follow(link, self.parseMateria)

	def parseMateria(self, response):
		link = response.url
		editoria = response.css("div.c-menu__item--active a::text").extract_first()
		editoria = editoria.lower()
		editoria = unidecode(editoria)

		if( editoria == "jogada" ):
			id_editoria = "svm.dn.cadernos.jogada.d"
		elif( editoria == "seguranca" ):
			id_editoria = "svm.dn.cadernos.policia.d"
		elif( editoria == "regiao" ):
			id_editoria = "svm.dn.cadernos.regional.d"
		elif( editoria == "pais" ):
			id_editoria = "svm.dn.cadernos.nacional.d"
		elif( editoria == "opniao" ):
			id_editoria = "svm.dn.opinion.d"
		elif( editoria == "metro" ):
			id_editoria = "svm.dn.cadernos.cidade.d"
		elif( editoria == "mundo" ):
			id_editoria = "svm.dn.cadernos.internacional.d"
		elif( editoria == "negocios" ):
			id_editoria = "svm.dn.cadernos.negocios.d"
		elif( editoria == "politica" ):
			id_editoria = "svm.dn.cadernos.policia.d"
		elif( editoria == "verso" ):
			id_editoria = "svm.dn.cadernos.verso.d"
		else:
			return False

		id_dn = link.split('-1.')[-1]
		
		titulo = response.css("h1.c-article__heading::text").extract_first()
		titulo = titulo.replace(":", "\:").replace("\n", "").replace("\t", "")

		autor = response.css("div.c-article__info span span::text").extract_first()
		autor = autor.replace(":", "\:").replace("\n", "").replace("\t", "")

		sub_titulo = response.css("h2.c-article__subheading::text").extract_first()
		sub_titulo = sub_titulo.replace(":", "\:").replace("\n", "").replace("\t", "")

		conteudo = response.css("div.c-article-content ::text").extract()

		conteudo = map(lambda n: n.strip(), conteudo)
		conteudo = filter(lambda n: n != "", conteudo)
		
		conteudo = ' '.join(conteudo)
		conteudo = conteudo.replace(":", "\:")
		conteudo = conteudo.replace("\t", "")
		conteudo = conteudo.replace("\n", "").replace("  ", " ")
		conteudo = conteudo.strip()

		if (conteudo == ""):
			return False

		image_url = response.css("div.c-article__photo-featured figure div div meta[itemprop='url']::attr(content)").extract_first()
		if ( image_url == None ):
			image_file = None
		else:
			r = requests.get(image_url)  
			with open('content/img_article_' + id_dn + '.jpg', 'wb') as f:
				f.write(r.content)
			image_file = 'img_article_' + id_dn + '.jpg'

		image_name = response.css("div.c-article__photo-featured figure div div picture::attr(data-alt)").extract_first()
		if ( image_name == None ):
			image_name = ""

		image_title = response.css("div.c-article__photo-featured figure div div picture::attr(data-title)").extract_first()
		if ( image_title == None ):
			image_title = ""

		image_caption = response.css("div.c-article__photo-featured figure figcaption.media__caption::text").extract_first()
		if (image_caption == None):
			image_caption = ""

		image_byline = response.css("div.c-article__photo-featured figure figcaption.media__caption span.media__credit::text").extract_first()
		if (image_byline == None):
			image_byline = ""

		materia = MateriaItem(
			link=link,
			editoria=editoria,

			id_article = "raspagem.diariodonordeste." + editoria + ".article" + id_dn,

			id_image = "raspagem.diariodonordeste." + editoria + ".article" + id_dn + ".image",
			image_name = image_name.replace(":", "\:").replace("\n", "").replace("\t", "").strip().encode().decode('utf-8'),
			image_title = image_title.replace(":", "\:").replace("\n", "").replace("\t", "").strip().encode().decode('utf-8'),
			image_caption = image_caption.replace(":", "\:").replace("\n", "").replace("\t", "").strip().encode().decode('utf-8'),
			image_byline = image_byline.replace(":", "\:").replace("\n", "").replace("\t", "").strip().encode().decode('utf-8'),
			image_file = image_file,

			id_editoria = id_editoria,
			titulo = titulo.strip().encode().decode('utf-8'),
			autor = autor.strip().encode().decode('utf-8'),
			sub_titulo = sub_titulo.strip().encode().decode('utf-8'),
			conteudo = conteudo.strip().encode().decode('utf-8'),
		)

		yield materia