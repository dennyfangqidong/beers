# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 18:24:50 2020

@author: Administrator
"""

import psycopg2
import re
# numpy for create uniform distribution to add for months
import numpy as np
# math for floor/cell
import math

#%%

conn = psycopg2.connect(host='49.235.53.241', port=5432,database = 'postgres',user='postgres')
cur = conn.cursor()
cur.execute("SELECT * FROM beer_brewdog")
columns = [str(x_elem) for x_elem in cur.description]
names = [re.findall(r"'(.*?)'", x, re.DOTALL)[0] for x in columns]
types = [int(re.findall(r"=(\d+)", x, re.DOTALL)[0]) for x in columns]
name_type_list = dict(zip(names,types))
cur.close()
conn.close()


#%%
# a list of all tags
fields = ['id', 'name', 'tagline', 'first_brewed', 'description', 'image_url', 'abv', 'ibu', 'target_fg', 'target_og', 'ebc', 'srm', 'ph', 'attenuation_level', 'volume', 'boil_volume', 'method', 'ingredients', 'food_pairing', 'brewers_tips', 'contributed_by']

# to find out columns that are lost, indicating returned jsons taht does not have specific columns
def find_loss_columns(element):
    loss_cols = []
    element_tags = element.keys()
    for ele_tag in element_tags:
        if ele_tag not in fields:
            loss_cols.append(ele_tag)
    for loss_col_elem in loss_cols:
        '''
        illustration of types:
            23 - int
            1082 - date
            25 - text
            1043 - varchar
            1700 - decimal
            3802 - jsonb
            1009 - text[][]
            
        '''
        get_type = name_type_list[loss_col_elem]
        if  get_type== 23:
            element[loss_col_elem] = -99999
        elif get_type == 1700:
            element[loss_col_elem] = -99999.99
        elif get_type== 1082:
            element[loss_col_elem] = '01/900'
        elif ((get_type == 1043) or (get_type==25)):
            element[loss_col_elem] = 'NoneGiven'
        elif get_type == 3802:
            element[loss_col_elem] = 'NoneGiven'
            # later row_to_json(row(element[loss_col_elem]))
        elif get_type == 1009:
            element[loss_col_elem] = []
            # later ARRAY[element[loss_col_elem]]::text
    return element


# if there is a None value, turn it into extreme/specific values, so that we could insert        
def kick_none(element):
    element_tags = element.keys()
    for ele_tag in element_tags:
        if element[ele_tag]==None:
            get_type = name_type_list[ele_tag]
            if  get_type== 23:
                element[ele_tag] = -9999
            elif get_type == 1700:
                element[ele_tag] = -9999.99
            elif get_type== 1082:
                element[ele_tag] = '01/900'
            elif ((get_type == 1043) or (get_type==25)):
                element[ele_tag] = 'Missing'
            elif get_type == 3802:
                element[ele_tag] = 'missing'
                # later row_to_json(row(element[loss_col_elem]))
            elif get_type == 1009:
                element[ele_tag] = []
    return element
            
# the date type generally 'mm/yyyy', but some dates are 'yyyy',therefore, we need to try
# split the date first, and if only 1 element included, than need to add month
def repair_dates(element):
    split_date = element['first_brewed'].split('/')
    if len(split_date)<2:
        month = math.floor(np.random.uniform(1,12,1))
        element['first_brewed'] = element['first_brewed']+'-'+str(month)
    else:
        element['first_brewed']=split_date[1]+'-'+split_date[0]
    return element           