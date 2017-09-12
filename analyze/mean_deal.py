# coding=utf-8

import sqlite3
import pandas as pd
import make_data
import log


# 找出10天内5日线首次突破20日线，且成交量翻倍的股票
# 参数target_date为分析日期，默认为最后一个交易日
def get_mean_deal(target_date=make_data.last_trade_date()[0]):
    con = sqlite3.connect('History.db')
    query1 = "select name from sqlite_master where type='table' order by name"
    stocklist = pd.read_sql(query1, con).name

    log_file = open("log/analyze.log", 'a+')
    result = []  # 保存抓取股票列表
    #last_trade_date = make_data.last_trade_date()[0]
    #last_trade_date = "2017-09-06"


    log.write(log_file, "开始抓取日线突破股票列表")
    #result_file.write(last_trade_date + ',')
    #result.append(target_date)

    for stock in stocklist:
        query2 = "select * from '%s' order by date" %stock
        df = pd.read_sql(query2, con)
        df = df.set_index('date')

        # 若交易记录少于10条，跳过
        if len(df) < 10:
            continue
        # 若无法找到目标日的交易数据（停牌），跳过
        if target_date not in df.index:
            continue
        # 若股票最后一条交易记录不是上一个交易日（停牌），跳过
        # if df.index[-1] != last_trade_date:
        #     continue

        df.index = pd.to_datetime(df.index)
        df = df["2017-01-01":target_date]  # 只取2017年至目标日的记录

        close = df.close
        mean5 = pd.rolling_mean(close, 5)
        mean20 = pd.rolling_mean(close, 20)
        if mean5[-1]>mean20[-1]:
            if int(df.ix[-1,"volume"]) > int(df.ix[-2,"volume"])*2:
                sign = True
                for i in range(-2,-10,-1):
                    if mean5[i] > mean20[i]:
                        sign = False
                if sign:
                    #result_file.write(stock + ',')
                    result.append(stock)

    log.write(log_file, "完成抓取日线突破股票列表，共获得%s只股票" % len(result))

    # 如果获取日期为现有记录的下一个交易日，则添加记录
    result_file = open('focus/mean_deal.csv', 'r')
    result_file_lines = result_file.readlines()
    result_file.close()
    if len(result_file_lines) != 0:  # 如果文件没有记录，直接加入记录
        last_recode_date = result_file_lines[-1].split(',')[0]
        if make_data.next_trade_date(last_recode_date) != target_date:
            return result

    log.write(log_file, "更新记录文件")
    result_file_lines.append(target_date + ',' + ','.join(result) + '\n')
    result_file = open('focus/mean_deal.csv', 'w')
    for line in result_file_lines:
        result_file.write(line)
    result_file.close()
    return result
