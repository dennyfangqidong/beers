# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:56:50 2020

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:50:09 2020

@author: Denny_Fang

Location of Webdriver: C:\ProgramData\webdriver (Firefox)
"""

#%%
# since the array in json file, and return in str, we need json to turn transform data
import json


#%%
# a function for fetching json data from website url
def fetch_json(driver,url):
    driver.get(url)
    # need to wait a little while for the page to load finished; later prepare...
    driver.implicitly_wait(30)
    # 选择“原始数据”的tab
    driver.find_element_by_id('rawdata-tab').click()
    driver.implicitly_wait(30)
    webpage_content = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/pre')
    webpage_dict = webpage_content.text
    webpage_json = json.loads(webpage_dict)
    # test for all the attributes of returned json files
    ''' 
    for details of test attributes meta data, see excel: beer_tags
    '''
#    for i in range(len(webpage_json)):
#        print("keys for %d: "%(i),webpage_json[i].keys())
#        print("keys count for %d"%(i),len(webpage_json[i].keys()))
    return webpage_json
    

#%%
# explore all the keys of current dictionary
