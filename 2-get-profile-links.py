#!/usr/bin/env python
#
# built with Python 2.7.8 on Mac OS X Yosemite
# built for http://journalismcourses.org/course/view.php?id=25
# that is, Data Visualization and Infographics with D3! 
# MIT License
#
# usage:
# run from the terminal with the command
# python 2-get-profile-links.py
#
import os, re, csv
from bs4 import BeautifulSoup

profile_links_set = set()

path = os.getcwd()

for dirpath, dirs, files in os.walk(path):
    for name in files:
        if name.endswith((".html")):

        	soup  = BeautifulSoup(open(dirpath + "/" + name), 'lxml')
        	#print soup

        	profile_links = soup.find_all('div', class_='author', 
        		attrs={'role': 'heading'})

        	for link in profile_links:
        		profile_links_set.add(link.a.get('href'))


with open('profile-links.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for link in profile_links_set:
    	wr.writerow([link])

f.close()