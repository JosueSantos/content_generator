# -*- coding: utf-8 -*-
import scrapy
import re

from content_generator.items import MateriaBackupItem


class DiarioBackupSpider(scrapy.Spider):
	name = 'diario-backup'
	allowed_domains = ['diariodonordeste.verdesmares.com.br']
	start_urls = ['https://diariodonordeste.verdesmares.com.br']
	index = 1

	def parse(self, response):
		loop = True

		while loop:
			self.index = self.index + 1
			link = 'https://diariodonordeste.verdesmares.com.br/servicos/-1.' + str(self.index)

			if self.index > 2555111:
				loop = False

			yield response.follow(link, self.parseMateria)

	def parseMateria(self, response):
		page_article = response.css("article.c-article").extract_first()

		if page_article is not None:
			pattern = re.compile(r'\s')

			link = response.url
			
			editoria = response.css("div.c-tools--editorial-article div a.c-tools__link ::text").extract_first()
			if editoria is not None:
				editoria = re.sub(pattern, ' ', editoria).replace("  ", " ").encode().decode('utf-8')
			
			titulo = response.css("h1.c-article__heading::text").extract_first()
			if titulo is not None:
				titulo = re.sub(pattern, ' ', titulo).replace("  ", " ").encode().decode('utf-8')

			sub_titulo = response.css("h2.c-article__subheading::text").extract_first()
			if sub_titulo is not None:
				sub_titulo = re.sub(pattern, ' ', sub_titulo).replace("  ", " ").encode().decode('utf-8')

			autor = response.css("div.c-article__info span span::text").extract_first()
			if autor is not None:
				autor = re.sub(pattern, ' ', autor).replace("  ", " ").encode().decode('utf-8')

			time = response.css("time.c-article__date-created::text").extract_first().strip()
			if time is not None:
				time = re.sub(pattern, ' ', time).replace("  ", " ").encode().decode('utf-8')

			tags = response.css("footer.c-article__footer div div.tags a::text").extract()
			if tags is not None:
				tags = ', '.join(tags)
				tags = re.sub(pattern, ' ', tags).replace("  ", " ").encode().decode('utf-8')

			link_rel = response.css("article.c-article div div div.c-article__main div.c-article-content p a::attr(href)").extract()
			link_rel_interno = response.css("article.c-article div div div.c-article__main div.c-article-content p a[href*='diariodonordeste.verdesmares']::attr(href)").extract()

			id_dn = link.split('-1.')[-1]
			date = time.split('/')[1].strip()
			time = time[0:5]

			conteudoHtml = str( response.css("div.c-article-content").extract_first() )
			conteudoHtml = re.sub(pattern, ' ', conteudoHtml).replace("  ", "").encode().decode('utf-8')

			conteudo = response.css("div.c-article-content ::text").extract()
			conteudo = map(lambda n: n.strip(), conteudo)
			conteudo = filter(lambda n: n != "", conteudo)

			conteudo = ' '.join(conteudo)
			conteudo = re.sub(pattern, ' ', conteudo).replace("  ", " ").encode().decode('utf-8')

			materia = MateriaBackupItem(
				link=link,
				editoria=editoria,
				titulo=titulo,
				sub_titulo=sub_titulo,
				autor=autor,
				time=time,
				date=date,
				link_rel=len(link_rel),
				link_rel_interno=len(link_rel_interno),
				id_dn=id_dn,
				tags=tags,
				conteudoHtml=conteudoHtml,
				conteudo=conteudo,
			)

			yield materia