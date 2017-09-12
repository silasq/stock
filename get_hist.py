# coding=utf-8

'''
批量获得所有股票历史数据
'''
import tushare as ts
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from datetime import *
import log
import make_data

log_file = open("log/get_hist.log", 'a+')
log.write(log_file,"开始更新股票数据!")

con = sqlite3.connect('History.db')
query1 = "select name from sqlite_master where type='table' order by name"
stocklist = pd.read_sql(query1, con).name
engine = create_engine('sqlite:///History.db', echo = False)

# count[0]:新增股票记录数
# count[1]:更新股票记录数
# count[2]:无需更新股票记录数
count = [0, 0, 0]

for stock in stocklist:
    query2 = "select * from '%s' order by date" % stock
    df = pd.read_sql(query2, con)
    df = df.set_index('date')

    if len(df) == 0:
        df = ts.get_k_data(stock, start="2000-01-01")
        df.to_sql(stock, engine, if_exists='append', index=False)
        count[0] += 1
        continue

    if datetime.now().hour < 15:
        today = datetime.now() - timedelta(days=1)
    else:
        today = datetime.now()

    last_trade_date = make_data.last_trade_date()[0]

    recode_date = df.ix[-1].name

    if last_trade_date != recode_date:
        try:
            df = ts.get_k_data(stock, start=str(pd.Timestamp(recode_date) + pd.Timedelta(days=1))[:10])
            if len(df) == 0:
                count[2] += 1
                continue
            df.to_sql(stock, engine, if_exists='append', index=False)
            count[1] += 1
        except Exception, e:
            log.write(log_file,e.message)
            continue
    else:
        count[2] += 1

log.write(log_file,"获取新股票%s个，成功更新股票%s个，无需更新股票%s个！" % (count[0], count[1], count[2]))
log.write(log_file,"完成更新股票数据！")
log_file.close()