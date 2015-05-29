#!/usr/bin/env python
#
# built with Python 2.7.8 on Mac OS X Yosemite
# built for http://journalismcourses.org/course/view.php?id=25
# that is, Data Visualization and Infographics with D3! 
# MIT License
#
# usage:
# run from the terminal with the command
# python 3-scrape-profiles.py
#
from requests import session
from bs4 import BeautifulSoup
import os, sys, csv, re, shutil, requests

profile_links_set = set()

with open('profile-links.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row[0]
        profile_links_set.add(row[0])

def login(user, pwd):
    authdata = {
        'action': 'login',
        'username': user,
        'password': pwd
    }
    with session() as ses:
        r = ses.post(baseurl + 'login/index.php', data=authdata)
        return ses

# add a string containing the base url for your school here
baseurl = 'http://journalismcourses.org/'
output_path = 'profiles/'

# prompt the user at the command line for a username and password
user = raw_input("username for " + baseurl + "? ")
pwd = raw_input("password? ")


#logging in
print "logging in..."
session = login(user, pwd)

def scrape(link_set, path):
    # check to see if the directories in the path string exist
    if not os.path.exists(path):
        #if not, create them
        os.makedirs(path)
    
    for link in link_set:
    
        r = session.get(link)
        
        if(r.status_code == 200):
            soup = BeautifulSoup(r.text, 'lxml')

            # extract the user id 
            # useful for naming the html and png files we will scrape
            user_id = re.search(r"(?<=user\/view\.php\?id=)\d*", link).group()

            # save the profile page as a .html file 
            #output_file = path + str(user_id) + ".html"
            #with open(output_file, 'w') as f:
            #    f.write(str(soup))
            #f.close()
            #print "page saved at " + output_file

            image_link = soup.find_all('img', class_='userpicture')[1].get('src')

            # save the profile image as a .png file
            output_file = path + str(user_id) + ".png"
            response = requests.get(image_link, stream=True)
            with open(output_file, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            print "image saved at " + output_file
    
        else:
            print 'ERROR: ' + str(r.status) + ' ' + r.reason
            sys.exit()

# scrape the profiles
scrape(profile_links_set,output_path)