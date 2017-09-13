# coding=utf-8

"""
获取所有股票全量信息，并保存在database/stock_basics.csv中
对比History.db数据库中的信息，对于没有记录的股票新建表
"""

import tushare as ts
from sqlalchemy import *
import os
import log
import make_data


def get():
    log_file = open("log/get_all_stock.log", 'a+')
    log.write(log_file,"get all stock info start!")

    # 若果database目录不存在，则新建
    if not os.path.exists('database'):
        os.makedirs('database')

    # 准备数据库连接
    engine = create_engine('sqlite:///database/History.db', echo=False)
    metadata = MetaData(engine)

    # 如果存在旧csv文件，则改名后备份，若备份失败则终止程序
    if os.path.exists("database/stock_basics.csv"):
        if os.system('mv database/stock_basics.csv basics_bak/stock_basics_`date "+%Y-%m-%d"`.csv') == 0:
            log.write(log_file, "stock_basics.csv backup complete!")
        else:
            log.write(log_file, "stock_basics.csv backup error!")
            return False

    df = ts.get_stock_basics()  # 获取数据
    log.write(log_file,"get stock basics data complete!")
    df.to_csv('database/stock_basics.csv')  # 保存至stock_basics.csv文件中
    log.write(log_file,"save stock basics data complete!")

    stocks = list(df.index)  # 获取股票代码
    stocks_old = engine.table_names()  # 从数据库中读取股票代码

    # 检查所有获取数据，对于不存在的股票代码，新建表
    for i in range(0,len(stocks)):
        code = make_data.num2stock(stocks[i],log_file)  # 为股票代码添加开头
        if not code:
            continue  # 若不能识别则跳过

        if code in stocks_old:
            continue  # 若股票代码以存在数据库中，则跳过

        Table(code, metadata,
              Column('date', DATE, primary_key=True),
              Column('open', REAL),
              Column('close', REAL),
              Column('high', REAL),
              Column('low', REAL),
              Column('volume', REAL),
              Column('code', REAL))

        metadata.create_all(engine)

        log.write(log_file,"new stock add : " + code)

    log.write(log_file, "get all stock info finish!")

    log_file.close()



