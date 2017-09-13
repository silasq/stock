# coding=utf-8


import tushare as ts
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
import log
import make_data
import progressbar


#
# 批量更新所有股票历史数据
#
def refresh_all():
    log_file = open("log/get_hist.log", 'a+')
    con = sqlite3.connect('database/History.db')
    query1 = "select name from sqlite_master where type='table' order by name"
    stocklist = pd.read_sql(query1, con).name
    engine = create_engine('sqlite:///database/History.db', echo=False)

    log.write(log_file, "开始更新股票数据!")

    # count[0]:新增股票记录数
    # count[1]:更新股票记录数
    # count[2]:无需更新股票记录数
    count = [0, 0, 0]

    # 准备进度条
    bar = 0;
    bar_total = len(stocklist)
    pbar = progressbar.ProgressBar(max_value= bar_total).start()

    for stock in stocklist:
        pbar.update(bar)  # 更新进度条
        bar += 1

        query2 = "select * from '%s' order by date" % stock
        df = pd.read_sql(query2, con)
        df = df.set_index('date')

        if len(df) == 0:
            df = ts.get_k_data(stock, start="2000-01-01")
            df.to_sql(stock, engine, if_exists='append', index=False)
            count[0] += 1
            continue

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

    pbar.finish()

    log.write(log_file,"获取新股票%s个，成功更新股票%s个，无需更新股票%s个！" % (count[0], count[1], count[2]))
    log.write(log_file,"完成更新股票数据！")
    log_file.close()