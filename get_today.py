'''
每日15点后执行以获取当日股票交易数据
'''

# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


import os
import tushare as ts
from sqlalchemy import *
import sqlite3
import pandas as pd
from datetime import *

con = sqlite3.connect('History.db')
query1 = "select name from sqlite_master where type='table' order by name"
stocklist = pd.read_sql(query1, con).name

engine = create_engine('sqlite:///History.db', echo = False)
metadata = MetaData(engine)

today = datetime.now()
if today.weekday() == 5:
    last_trade_date = str(pd.Timestamp(datetime.now()) - pd.Timedelta(days=1))[:10]
elif today.weekday() == 6:
    last_trade_date = str(pd.Timestamp(datetime.now()) - pd.Timedelta(days=2))[:10]
else:
    if datetime.now().hour < 15:
        exit(0)
    else:
        last_trade_date = str(pd.Timestamp(datetime.now()))[:10]

#if os.path.exists(""):

df = ts.get_today_all()
df.to_csv("today2.csv")
df = pd.read_csv("today2.csv",header=0,index_col=0,dtype={'code':str})

for i in range(0,len(df)):
    code = df.ix[i,'code']

    if code.startswith("60"):
        code = "sh" + code
    elif code.startswith("00") or code.startswith("30"):
        code = "sz" + code
    else:
        print "error : unknow code " + code
        continue

    today_data =  df.ix[i:i,["open","trade","high","low","volume"]]
    if today_data.ix[0,"open"] == "0.0":
        continue
    today_data.rename(columns={'trade':'close'}, inplace = True)
    today_data["code"] = code

    today_data["date"] = last_trade_date

    today_data["volume"] = int(today_data["volume"]/100)


    #today_data = today_data.set_index("date")

    today_data.to_sql(code, engine, if_exists='append', index=False)

    print today_data