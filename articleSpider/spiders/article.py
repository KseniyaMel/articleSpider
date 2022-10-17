#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 23:24:24 2022

@author: kseniamelihova
"""
import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
from articleSpider.items import Article


class ArticleSpider(scrapy.Spider):
    name='article'
    url='https://cyberleninka.ru/search'
    search ='?q=web'

    def start_requests(self):
        yield SeleniumRequest(url=self.url+self.search, callback=self.parse)

  
    def parse(self, response):
        articleItem = Article()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find('ul',id='search-results').findChildren()
        for article in articles:
            st = article.prettify()
            lisoup = BeautifulSoup(st, "html.parser")
            try:
                liname = lisoup.find('h2').findChildren()[0]
                liau = lisoup.find('span')
                if liname != None and liau != None:
                    articleItem['title'] = ' '.join(liname.text.replace('\n', '').split())
                    articleItem['href'] = self.url+liname.get('href')
                    articleItem['author'] = liau.text.replace('\n\"', '').strip()
                    yield articleItem
            finally:
                continue

    
        

