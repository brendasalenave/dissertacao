# -*- coding: utf-8 -*-
#!/usr/bin/envpython3

import requests, bs4, re
import urllib3
import unicodedata
from string import punctuation
from string import digits
import time
import csv
import os

class Extraction(object):
    """docstring for Extraction."""
    def __init__(self, url_pois, url_city):
        super(Extraction, self).__init__()
        self.url_pois = url_pois
        self.url_city = url_city

    def write_file(self,establishment, category, average, total, lat, long, commentList,dateList,agreeList,disagreeList, usersList, genderList, tips):
        if not os.path.exists('./foursquare_data.csv'):
            with open('foursquare_data.csv', 'w', newline='') as outputfile:
                writer = csv.writer(outputfile, delimiter=',', quotechar='"')
                writer.writerow(['Establishment','Category','Average Ratings','Total Ratings','Latitude','Longitude','Comment', 'Date','Comment Votes Up', 'Comment Votes Down', 'User', 'Gender Appraiser', 'Tips Appraiser'])
                for a,b,c,d,e,f,g in zip(commentList,dateList,agreeList,disagreeList,usersList ,genderList,tips):
                    writer.writerow([establishment,category,average,total,lat, long, a, b, c, d, e, f, g])
        else:
            with open('foursquare_data.csv', 'a', newline='') as outputfile:
                writer = csv.writer(outputfile, delimiter=',', quotechar='"')
                for a,b,c,d,e,f,g in zip(commentList,dateList,agreeList,disagreeList,usersList ,genderList,tips):
                    writer.writerow([establishment,category,average,total,lat, long, a, b, c, d, e, f, g])


    def poi_data_extraction(self):
        print('Downloading page: %s...\n'% self.url_pois)

        res=requests.get(self.url_pois,timeout=None)
        #res.raise_for_status()
        if res.status_code != 500:
            soup=bs4.BeautifulSoup(res.text,'lxml')
            #establishment, category, average, ratings, latitude, longitude = [], [], [], [], [], []
        average = []
        e_checked = []
        e_not_checked = []

        # Get the name of the establishment
        for x in soup.find_all('div', class_="venueName"):
                name = re.search('_blank\">(.)*</a>',str(x))
                name = name.group(0).split('>')[1].split('<')[0]
                name = name.replace(';','')
                print(name)
                #nome do estabelecimento
                e_name = name

                page = re.search('href=\"(.)*\"',str(x))
                page = page.group(0).split('\"')[1]
                page = 'https://pt.foursquare.com' + str(page)

                userpages = self.data_extraction(page,e_name,pde_1=True)
                e_checked.append(e_name)
                time.sleep(5)

                #get new places
                e_not_checked = e_not_checked + self.poi_data_extraction_2(userpages)

        e_not_checked = list(set(e_not_checked))
        new_establishments = []
        for i in e_not_checked:
            if i[0] not in e_checked:
                print('->',i,type(i))
                new_establishments.append((i[0],i[1]))
                e_checked.append(i[0])

        for i in new_establishments:
            self.data_extraction(i[1], i[0])
        time.sleep(2)


    def poi_data_extraction_2(self, userpages):
        # print("starting phase 2")
        e_data = set()
        for x in userpages:
            res_=requests.get(x+'?all-tips',timeout=None)
            #req_.raise_for_status()
            if(res_.status_code != 500):
                soup = bs4.BeautifulSoup(res_.text,'lxml')
                for y in soup.find_all('div', class_='tipVenueDetails'):
                    y = str(y)
                    if 'Gramado' in y:
                        e_page = y.split('href=\"')[1]
                        e_page = e_page.split('\"')[0]
                        e_page = 'https://pt.foursquare.com' + str(e_page)
                        e_name = y.split('href=\"')[1].split('>')[1].split('<')[0]
                        # print('NOME:',e_name,'\n\n')
                        e_data.add((e_name, e_page))

        return list(e_data)

    def data_extraction(self, page, establishment, pde_1=False):
        category, average, ratings, latitude, longitude = [], [], [], [], []

        res_=requests.get(page,timeout=None)
        #res_.raise_for_status()
        if res_.status_code != 500:
            originalSoup = bs4.BeautifulSoup(res_.text,'lxml')
            old_sort = '<li data-sort="popular"  class="selected"><span class="sortLink">Popular</span></li><li data-sort="recent" >'
            new_sort = '<li data-sort="popular"> <span class="sortLink">Popular</span></li><li data-sort="recent"  class="selected">'

            soup_ = bs4.BeautifulSoup(str(originalSoup).replace(old_sort,new_sort),'lxml')
            # Category of establishment
            for y in soup_.find_all('span',class_="categoryName"):
                categoryName = str(y).split('>')[1].split('<')[0]
                print('Category:', categoryName)
                category = categoryName
                break

            # Average of ratings
            for y in soup_.find_all('span',itemprop="ratingValue"):
                rating = str(y).split('>')[1].split('<')[0]
                print('average rating:', rating)
                average = rating

            # Total of ratings
            for y in soup_.find_all('div',class_="numRatings"):
                total = str(y).split('>')[1].split('<')[0]
                print('total ratings:', total)
                ratings = total

            # Lozalization: lat and long
            for y in soup_.find_all('span',class_="venueDirectionsLink"):
                lat,long = str(y).split('=')[4].split('\"')[0].replace(',',' ').split()
                print('Localização -> ' + 'lat:' + lat + ' long:' + long)
                latitude = lat
                longitude = long

            disagreeList, agreeList, commentList, genderList, tips, dateList = [], [], [], [], [], []

            # Comments
            for y in soup_.find_all('div',class_="tipText"):
                tip_text = str(y).split('</div')[0].split('\"tipText\">')[1]
                tip_text = re.sub('<(.)*?>',' ',tip_text.replace('</span>',''))
                tip_text = tip_text.replace(';','')
                commentList.append(tip_text)

            for y in soup_.find_all('span',class_='tipDate'):
                tip_date = str(y).split('</span')[0].split('>')[1]
                dateList.append(tip_date)

            for y in soup_.find_all('li',class_="tip tipWithLogging useTipUpvotes "):
                idComment = str(y).split('id=\"')[1].split('\"')[0]

                text = soup_.get_text()
                r = re.compile('%s.*?Count\":\d+,\"user\":.*?\"gender\":\"\w+\"'%idComment,re.DOTALL)

                for m in r.finditer(text):
                    t = m.group(0)
                    # Comment votes up
                    m = re.search('\"agreeCount\":\d+', t)
                    if m: agreeList.append(m.group(0).split(':')[1])
                    # Comment votes down
                    m = re.search('\"disagreeCount\":\d+', t)
                    if m: disagreeList.append(m.group(0).split(':')[1])
                    # Appraiser gender
                    m = re.search('\"gender\":\"\w+\"', t)
                    if m: genderList.append(m.group(0).split(':')[1].replace('\"',''))
                    break

            userpages = []
            usersList = []
            for y in soup_.find_all('span',class_="userName"):
                usersLinks = y.find_all('a')
                for user in usersLinks:
                    print("-> text user:", str(user))
                    user_url = str(user).split('\"')[1]
                    userpage = 'https://pt.foursquare.com' + str(user_url)
                    userpages.append(userpage)

            for y in userpages:
                req_=requests.get(y,timeout=None)
                #req_.raise_for_status()
                if(req_.status_code != 500):
                    _soup = bs4.BeautifulSoup(req_.text,'lxml')
                    for z in _soup.find_all('span', class_='stat'):
                    #Total of tips given by the appraiser
                        if 'Dicas' in str(z):
                            tips.append(str(z).split('>')[2].split('<')[0])
                    for z in _soup.find_all('h1', class_='name'):
                        username = str(z).split('>')[1].split('<')[0]
                        old_len = len(usersList)
                        usersList.append(username)


            for g,a,b,c,d,e,f in zip(usersList,commentList,agreeList,disagreeList,genderList,tips,dateList):
                print ('\n\nUser:' + g + '\n' +'Comment:'+ a +'\n' + 'Date:'+ f +'\n' + 'agreeCount:' + b + '\n' 'disagreCount:' + c + '\n'+ 'gender:' + d + '\n' + 'tips:' + e)
            self.write_file(establishment, category, average, ratings, latitude, longitude,commentList,dateList,agreeList,disagreeList,usersList,genderList,tips)
            print('\n\n')
            if pde_1:
                return userpages

    def city_data_extraction(self):
        data = []
        print('Downloading page: %s...\n'% self.url_city)

        res=requests.get(self.url_city,timeout=None)
        res.raise_for_status()
        if res.status_code != 500:
            soup=bs4.BeautifulSoup(res.text,'lxml')

        for x in soup.find_all('meta',property="og:title"):
            text = str(x).split(': ')[1].split(' |')[0]
            data.append('Cidade\n\n'+text)

        for x in soup.find_all('div',class_="tab-pane active"):
            text = re.search(r'<p>.*<\/p>', str(x), flags=re.DOTALL)
            text = text.group(0)
            text = re.sub('<p>|<\/p>','',text)
            text = re.sub(' +',' ',text)
            text = re.sub('\n','',text)
            data.append('Descricao\n\n'+text)

        for x in soup.find_all('div',class_="widget"):
            r = re.sub('<[^>]+?>','',str(x))
            r = re.sub('[ ]{2,}',' ',r)

            data.append(r)

        # print(data)
        self.write_city_file(data)

    def write_city_file(self,data):
        with open('city_data.csv', 'w', newline='') as outputfile:
            writer = csv.writer(outputfile, delimiter=',', quotechar='"')
            for x in data:
                line = [i for i in x.split('\n') if len(i)>0]
                writer.writerow(line)
