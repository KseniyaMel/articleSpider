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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ArticleSpider(scrapy.Spider):
    name='article'
    url='https://cyberleninka.ru'
    search ='/search?q=web'
    pages = '&page='
    pages_count = ['1','2','3']

    def start_requests(self):
        return [SeleniumRequest(url=self.url+self.search+self.pages+page, callback=self.parse, wait_time=10) for page in self.pages_count]

  
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
                    articleItem['author'] = liau.text.replace('\n', '').strip().replace('"','')
                    yield articleItem
            finally:
                continue

    
        

