import re
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

import sys
sys.path.append("../Startup_Ideas")
from db_repo.db_handle import *


# set categories to parse 
list_cats = ['analytics', 'abtesting', 'advertising', 'advice', 'affiliate', 
             'automation', 'billing', 'blogging', 'books', 'contests', 'conversion',
             'crms', 'customerdiscovery', 'development', 'domains', 'emailtools',
             'espionage', 'filetransfer', 'financial', 'forms', 'fundraising', 'graphics',
             'growthhacking', 'helpdesks', 'hiring', 'hosting', 'leads', 'legal'
             'listbuilding', 'listingservices', 'logos', 'marketing', 'misc', 'mockups',
             'monitoring', 'networking', 'newslettering', 'organization', 'outreach',
             'paymentsolutions', 'podcasts', 'popups', 'prelaunchtraction', 'productivity',
             'research', 'sales', 'salesfunnels', 'schedulers', 'seo', 'sitebuilders',
             'sitesupport', 'socialmedia', 'stockphotos', 'swag', 'telecom', 'templates',
             'traction', 'userchat', 'video', 'virtualassistants', 'webinars', 'writing']
chosen_cats = ['analytics', 'financial']

def get_links(page) -> list:
    cat = requests.get(page)
    soup = BeautifulSoup(cat.text, 'html.parser')
    cat_hrefs = []
    for link in soup("a", "post-card-content-link", href=True):
        cat_hrefs.append(link['href'])
    cat_hrefs = list(dict.fromkeys(cat_hrefs))
    return cat_hrefs

def get_s_info(s_link):
    s_title = ''
    s_desc = ''
    s_tags = ''
    s_link = s_link

    soup = requests.get(s_link)
    soup = BeautifulSoup(soup.text, 'html.parser')
    
    # get startup info
    s_title = soup.find_all(class_="fl-heading-text")[0].text
    s_desc = soup.find_all('p')[1].text
    s_tags = re.sub('\n|\s+', '', soup.find_all(class_="fl-icon-wrap")[-1].text).replace(',', ", ")
    
    return (s_title, s_desc, s_tags, s_link)

for cat in chosen_cats:

    cat_hrefs = get_links(f'https://startupresources.io/collection/{cat}/')

    for cat_href in cat_hrefs:
        insert_values = [*get_s_info(cat_href), cat, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        insert_values = tuple(list(map(insert_values.__getitem__, [0, 4, 1, 2, 3, 5])))

        try:
            add2db('startups_info', ('title', 'category', 'description', 'tags', 'link', 'time_added'), insert_values)
        except Exception as e:
            pass
        
        result = get_s_info(cat_href)
        print(result)
        
        time.sleep(2)
