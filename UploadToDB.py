import pandas as pd
from sqlalchemy import VARCHAR, create_engine
import pymysql
import os
import json
import config


file = "fighters_small.json"
json_data=open(file).read()
json_obj = json.loads(json_data)

df = pd.read_json('fighters_small.json')

df_t = df.T

df_t.reset_index(drop=True, inplace=True)


print(df_t)


engine = create_engine('mysql+pymysql://' + config.db_user + ':' + config.db_password + '@' + config.db_host + '/db')
engine1 = create_engine('mysql+pymysql://root:jj33My99@192.168.2.27/db')

con = pymysql.connect(host = config.db_host,user = config.db_user,passwd = config.db_password,db = 'db')

df_t.to_sql(con=engine1, name='fighters', if_exists='replace', index=False)

'''
# connect to MySQL

cursor = con.cursor()


# parse json data to SQL insert
for key in json_obj:
    name = json_obj[key]['name']
    weight = json_obj[key]['weight']
    cursor.execute("INSERT INTO fighters (name,	weight) VALUES (%s,	%s)", (name,	weight))



con.commit()
con.close()
'''



# do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val