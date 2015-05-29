#!/usr/bin/env python
#
# built with Python 2.7.8 on Mac OS X Yosemite
# built for http://journalismcourses.org/course/view.php?id=25
# that is, Data Visualization and Infographics with D3! 
# MIT License
#
# usage:
# run from the terminal with the command
# python 1-scrape-forums.py
#
from requests import session
from bs4 import BeautifulSoup
import os, sys

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

# prompt the user at the command line for a username and password
user = raw_input("username for " + baseurl + "? ")
pwd = raw_input("password? ")


#logging in
print "logging in..."
session = login(user, pwd)

def scrape(forums, path):
    # check to see if the directories in the path string exist
    if not os.path.exists(path):
        #if not, create them
        os.makedirs(path)
    
    for forumID in forums:
    
        r = session.get(baseurl + 'mod/forum/view.php?id=' + forumID)
        
        if(r.status_code == 200):
            soup = BeautifulSoup(r.text, 'lxml')
        
            posts = soup.find_all('td', class_='topic starter')
        
            # loop through the posts on a forum page 
            # visit each post and save the thread as a .html file
            print "scraping posts from forumID " + forumID
            
            for post in posts:
                r = session.get(post.a.get('href'))
                if(r.status_code == 200):
                    soup = BeautifulSoup(r.text, 'lxml')
                    output_file = path + str(soup.find("input", attrs={"name": "d"}).get('value')) + ".html"
                    print "page saved at " + output_file
                    with open(output_file, 'w') as f:
                        f.write(str(soup))
                    f.close()
    
        else:
            print 'ERROR: ' + str(r.status) + ' ' + r.reason
            sys.exit()

# uncomment a line in the parameter list to save the pages for that discussion forum.
# you can identify the forum by the name of the folder 
# by the value assigned to the 'path' key 
#
# to adapt this script to another course, visit the page for each forum in a browser
# and note the forumdID
#
# if your course has so many forums that this manual indexing approach becomes impractical, 
# identify something unique about the links to individual forums and select them 
# using BeautifulSoup. Then, you can pass the selection to requests to visit 
# each forum page, like we do with individual posts.
#
parameters = [

    #{ 'forums':['4160'], 'path':"resources/" },
    #{ 'forums':['4024'], 'path':"course-news/" },
    #{ 'forums':['4029'], 'path':"student-lounge/" },
    #{ 'forums':['4025'], 'path':"questions-for-instructors/" },
    #{ 'forums':['4352', '4145', '4146'], 'path':"1/discussion-forum/" },
    #{ 'forums':['4267', '4354', '4353'], 'path':"1/technical-forum/" },
    #{ 'forums':['4144', '4162', '4161'], 'path':"1/exercise-forum/" },
    #{ 'forums':['4360', '4391', '4392'], 'path':"2/discussion-forum/" },
    #{ 'forums':['4372', '4373', '4374'], 'path':"2/technical-forum/" },
    #{ 'forums':['4364', '4393', '4394'], 'path':"2/exercise-forum/" },
    #{ 'forums':['4431', '4433', '4432'], 'path':"3/discussion-forum/" },
    #{ 'forums':['4435', '4436', '4437'], 'path':"3/technical-forum/" },
    #{ 'forums':['4439', '4470', '4471'], 'path':"3/exercise-forum/" },
    #{ 'forums':['4507', '4497', '4496'], 'path':"4/discussion-forum/" },
    #{ 'forums':['4482', '4483', '4484'], 'path':"4/technical-forum/" },
    #{ 'forums':['4515', '4499', '4498'], 'path':"4/exercise-forum/" },
    #{ 'forums':['4480', '4517', '4516'], 'path':"5/discussion-forum/" }, 
    #{ 'forums':['4509', '4510', '4511'], 'path':"5/technical-forum/" }, 
    #{ 'forums':['4534', '4518', '4519'], 'path':"5/exercise-forum/" },
    #{ 'forums':['4528', '4537', '4538'], 'path':"6/discussion-forum/" },
    #{ 'forums':['4530', '4531', '4532'], 'path':"6/technical-forum/" },
    #{ 'forums':['4495', '4539', '4540'], 'path':"6/exercise-forum/" }

]

for p in parameters:
    scrape(p['forums'],p['path'])