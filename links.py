#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:47:09 2021

@author: mattia
"""
import requests
from bs4 import BeautifulSoup
from sys import exit

CAS = '7664-41-7'
molecule = 'Sodium iodate'

url='https://www.sigmaaldrich.com/catalog/search?interface=CAS%20No.&term='+CAS+'&N=0&lang=it&region=IT&focus=product&mode=mode+matchall'
page = requests.get(url)

soup=BeautifulSoup(page.content, 'html.parser')

list_tags = soup.find_all(class_="productContainer-inner")

list_tags[0].find_all("h2")

#divs = soup.find_all('div')

exit()
links = []

for link in soup.find_all('a', href=True):
    links.append(link['href'])

product_links = []

for link in links:
    if link.startswith('/catalog/product/'):
        link = link.split('?')[0]
        link = 'https://www.sigmaaldrich.com' + link + '?lang=it&region=IT'
        product_links.append(link)
        
unique = set(product_links)

test = list(unique)[0]

url = test
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# check here

#use CAS to change search

#then provide molecule name and grades

#molecule name is in productContainer clearfix/searchResultSubstanceBlock clearfix classmethod

#extract three search parameters from SDS javascript link

#build search query with https://www.sigmaaldrich.com/MSDS/MSDS/PleaseWaitMSDSPage.do?language=&country=IT&brand=SIAL&productNumber=402923&PageToGoToURL=https%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fsearch%3Finterface%3DCAS%2520No.%26term%3D79-11-8%26N%3D0%26lang%3Dit%26region%3DIT%26focus%3Dproduct%26mode%3Dmode%2Bmatchall

#find pdf in page

#look for c:set var="brandName" -> msdsContentDiv -> ... -> msdsLinkDiv -> iframe style ... src=''
        



