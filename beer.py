# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:50:09 2020

@author: Denny_Fang

Location of Webdriver: C:\ProgramData\webdriver (Firefox)
"""

#%%

# libs needed

import selenium
# usually, you need to save Firefox Webdriver in Anaconda/python installation path
from selenium import webdriver

import json

import psycopg2

import beerproj

import dirtyworks

#%%
# open the test webdriver, just for the convenience of test purpose
driver_main = webdriver.Firefox()


#%%
        
# create pgsql tables
# now connect to our created database
conn = psycopg2.connect(host='49.235.53.241', port=5432,database = 'postgres',user='postgres',password='')
cur = conn.cursor()

# this is how we suppose to create the database: 
# with first level json attribute - in corresponding data type(int,varchar, etc)
# for secondary and lower level json attributes - saved as json type
# technically, our database is no longer a conventional relational database
# the reason behind is because json is semi-structural data


# table columns/attributes illustration key points:
''' 
table attribute illustrations
See excel  - beer_tags.excel
'''

#A table has been created in my remote pc hosted by Tcloud
SQL_CreateTable = """CREATE TABLE IF NOT EXISTS beer_Brewdog(
id int PRIMARY KEY,
name varchar(100),
tagline varchar(100),
first_brewed date,
description text,
image_url varchar(60),
abv decimal,
ibu decimal,
target_fg decimal,
target_og decimal
,ebc decimal,
srm decimal,
ph decimal,
attenuation_level decimal,
volume jsonb,
boil_volume jsonb,
method jsonb,
ingredients jsonb,
food_pair text[][],
brewer_tips text,
contributed_by varchar(100));"""

cur.execute(SQL_CreateTable)

SQL_COMMIT = "COMMIT"
cur.execute(SQL_COMMIT)

cur.close()
conn.close()
#%%     
# connect to database
conn = psycopg2.connect(host='49.235.53.241', port=5432,database = 'postgres',user='postgres',password='')
cur = conn.cursor()

# getting data and save to db
    
# this is api for generate random links
url = 'https://api.punkapi.com/v2/beers/random'

fields = ['id', 'name', 'tagline', 'first_brewed', 'description', 'image_url', 'abv', 'ibu', 
  'target_fg', 'target_og', 'ebc', 'srm', 'ph', 'attenuation_level', 'volume', 
  'boil_volume', 'method', 'ingredients', 'food_pairing', 'brewers_tips', 'contributed_by']

# x indicates how many times you want to execute the random fetch
x = 100
ctn = 0
# how many consecutive times that the returned value already been inserted into database
ctn_non_execute = 0
db_prepare_json = []
saved_json_id = []
# the main part, 
# get non-repetative data for 100 times 
while ctn<x:
    temp_db_json = beerproj.fetch_json(driver_main,url)[0]
    # this try is to prevent less than 100 information left
    if ctn_non_execute <=15:
        if temp_db_json['id'] not in saved_json_id:
            # if value not repeated, clean None/missing column values
            dirtyworks.find_loss_columns(temp_db_json)
            dirtyworks.kick_none(temp_db_json)
            dirtyworks.repair_dates(temp_db_json)
            db_prepare_json.append(temp_db_json)
            saved_json_id.append(temp_db_json['id'])
            # insert data into db
            add_tuple = []
            for index, (key, value) in enumerate(temp_db_json.items()):
                add_tuple.append(json.dumps(value))
            add_tuple[3]=add_tuple[3].strip('"')
            insert_query = """INSERT INTO beer_Brewdog VALUES 
            (%s, %s, %s, to_date(%s,'yyyy-mm'), %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, ARRAY[%s], %s, %s) 
            ON conflict(id) DO NOTHING;"""
            cur.execute(insert_query, add_tuple)
            commit_query = "COMMIT;"
            cur.execute(commit_query,commit_query)
            ctn += 1
            ctn_non_execute = 0
        else:
            print('the id already saved in: ',saved_json_id)
            ctn_non_execute +=1
            pass
    else:
        break


print("%d rows inserted, while we want to insert %d rows"%(len(db_prepare_json),x))    
cur.close()
conn.close()
#%%
# a test case: if any beers first brewed before Jan 2013:

Separater = "$"*21
print (Separater+"Below shows beers first brewed before Jan 2013"+Separater)
conn = psycopg2.connect(host='49.235.53.241', port=5432,database = 'postgres',user='postgres')
cursor = conn.cursor()
select_query = "SELECT ingredients FROM beer_Brewdog where first_brewed <= to_date('2013-01','yyyy-mm');"
cursor.execute(select_query)
x = cursor.fetchall();
for xi in x:
    print(xi)

print (Separater+"Below shows all rows included"+Separater)

count_query = "SELECT COUNT(*) FROM beer_Brewdog;"
cursor.execute(count_query)
y = cursor.fetchall();
print(y[0])
    
#%%
cur.close()
conn.close()
