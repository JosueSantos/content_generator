# Gerador de arquivos .Content

---
> Raspagem de informações das matérias do Diário do Nordeste
>
> Endereços podem ser informados pelo arquivo **urls.csv**
>
> **O arquivo csv deve possuir cabeçalho**
>
> Clicando no ATUALIZAR_DADOS_DIARIO_DO_NORDESTE.py
>
> Após o carregamento, as informações estarão no arquivo **materias.content**


## Raspador Web em Python

##### Utiliza o Scrapy
![](https://scrapy.org/favicons/apple-touch-icon-180x180.png)

###### Instalação

* instale o python e a biblioteca scrapy
* pip install scrapy
* pip install requests
* pip install unidecode
* pip install pymongo


Os comandos abaixo podem ser executados:

* scrapy runspider spider_web/spiders/diario_nordeste.py
> Raspagem de informações das materias do Diario do Nordeste
>
> Endereços podem ser informados pelo arquivo **urls.csv**
>
> **O arquivo csv deve possuir cabeçalho**
>
> Clicando no ATUALIZAR_DADOS_DIARIO_DO_NORDESTE.py
>
> Após o carregamento, as informações estarão no arquivo **materias.content**