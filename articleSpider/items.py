import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    href = scrapy.Field() 
