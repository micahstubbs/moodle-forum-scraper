#!/usr/bin/env python
#
# built with Python 2.7.8 on Mac OS X Yosemite
# built for http://journalismcourses.org/course/view.php?id=25
# that is, Data Visualization and Infographics with D3! 
# MIT License
#
# usage:
# run from the terminal with the command
# python get-blocks-links.py
#
import os, re, csv
from bs4 import BeautifulSoup

block_links_set = set()

path = os.getcwd()

for dirpath, dirs, files in os.walk(path):
    for name in files:
        if name.endswith((".html")):

            soup  = BeautifulSoup(open(dirpath + "/" + name), 'lxml')
        	#print soup

            # the regex to find all bl.ocks links
            # http:\/\/bl\.ocks\.org\/[\w\d]*\/[\w\d]*

            block_links = soup.find_all(text=re.compile(r"http:\/\/bl\.ocks\.org\/[\w\d]*\/[\w\d]*"))

            for link in block_links:
                block_links_set.add(link.encode('utf-8'))

with open('block-links-raw.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for link in block_links_set:
        wr.writerow([link])

f.close()