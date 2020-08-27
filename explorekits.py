# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:51:28 2020

@author: Administrator
"""
import beerproj

import json

# driver_longest_name = webdriver.Firefox()

# used for find the longest element length for str of each 

def find_longest_length(driver,tag,n):
    url_start = 'https://api.punkapi.com/v2/beers?page='
    url_end = '&per_page=80'
    max_length = 0
    for i in range(n):
        url = url_start+str(i+1)+url_end
        temp_db_json = beerproj.fetch_json(driver,url)
        for x in temp_db_json:
            try:
                if type(x[tag]) is str:
                    len_mod = len(x[tag])
                # this is actually not needed, but for illustration, if a returned type is json,
                # after json.loads(), the returned value would be dict
                elif type(x[tag]) is (int or float):
                    len_mod = x[tag]
                elif type(x[tag]) is dict:
                    len_mod = len(x[tag])
                elif type(x[tag]) is None:
                    len_mod = 0
                else:
                    print("there is unexpected type: ",type(x[tag]));
                    break
                if (len_mod>max_length):
                    max_length = len_mod
            except Exception as e:
                pass
                print('Ooops..., the %s error happened!'%(e))
                print('Place of error: ',x['id'])
        driver.implicitly_wait(30)
    return max_length
        
# for detect values of all tags        
def get_all_tag_value(driver,tag,n):
    url_start = 'https://api.punkapi.com/v2/beers?page='
    url_end = '&per_page=80'
    tag_list = []
    for i in range(n):
        url = url_start+str(i+1)+url_end
        temp_db_json = beerproj.fetch_json(driver,url)
        for x in temp_db_json:
            try:
               tag_value = x[tag]
               if (tag_value not in tag_list):
                   tag_list.append(tag_value)
            except Exception as e:
                pass
                print('Ooops..., the %s error happened!'%(e))
                print('Place of error: ',x['id'])
        driver.implicitly_wait(30)
    return(tag_list)


# for find the most thorough tag names
# since this should work for whole db, no need to limit to n pages
def get_max_tags(driver):
    try:
        url_start = 'https://api.punkapi.com/v2/beers?page='
        url_end = '&per_page=80'
        tag_list = []
        for i in range(6):
            url = url_start+str(i+1)+url_end
            temp_db_json = beerproj.fetch_json(driver,url)
            for x in temp_db_json:
                keys = list(x.keys())
                for key_elem in keys:
                    if key_elem not in tag_list:
                        tag_list.append(key_elem)
            driver.implicitly_wait(30)
        return tag_list
    except Exception as e:
        print('Ooops..., the %s error happened!'%(e))
        print('Place of error: ',x)
        pass

# for test whether none value exists in current tag
def test_none(driver,tag,n):
    test_list = get_all_tag_value(driver,tag,n)
    print(sum(x is None for x in test_list))


# used for list all keys in any json type and the depth of the json, since json.load get dic, dict_a should be dictionary
key_list = []
def get_dict_allkeys(dict_a):
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        # 如果为字典类型，则提取key存放到key_list中
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            key_list.append(temp_key)
            get_dict_allkeys(temp_value)  # 自我调用实现无限遍历
    elif isinstance(dict_a, list):
        # 如果为列表类型，则遍历列表里的元素，将字典类型的按照上面的方法提取key
        for k in dict_a:
            if isinstance(k, dict):
                for x in range(len(k)):
                    temp_key = list(k.keys())[x]
                    temp_value = k[temp_key]
                    key_list.append(temp_key)
                    get_dict_allkeys(temp_value) # 自我调用实现无限遍历
    keys_list = set(key_list)
    return len(keys_list),keys_list
def get_json_keys(driver,tag,n):
    url_start = 'https://api.punkapi.com/v2/beers?page='
    url_end = '&per_page=80'
    max_depth = 0
    json_keys_all = []
    for i in range(n):
        url = url_start+str(i+1)+url_end
        temp_db_json = beerproj.fetch_json(driver,url)
        for x in temp_db_json:
            try:
               tag_value = x[tag]
               depth,json_keys = get_dict_allkeys(tag_value)
               for json_key in json_keys:
                   if json_key not in json_keys_all:
                       json_keys_all.append(json_key)
               if depth>max_depth:
                   max_depth = depth
            except Exception as e:
                pass
                print('Ooops..., the %s error happened!'%(e))
                print('Place of error: ',x['id'])
        driver.implicitly_wait(30)
    return json_keys_all,max_depth
            

