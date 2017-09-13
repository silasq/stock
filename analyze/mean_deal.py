# coding=utf-8

import sqlite3
import pandas as pd
import make_data
import log
import progressbar


# 找出10天内5日线首次突破20日线，且成交量翻倍的股票
# 参数target_date为分析日期，默认为最后一个交易日
def get_mean_deal(target_date):
    # 设置默认值，无法设为默认参数因为第一次运行会报错
    if target_date == '':
        target_date = make_data.last_trade_date()[0]

    con = sqlite3.connect('database/History.db')
    query1 = "select name from sqlite_master where type='table' order by name"
    stocklist = pd.read_sql(query1, con).name

    log_file = open("log/analyze.log", 'a+')
    result = []  # 保存抓取股票列表

    log.write(log_file, "开始抓取%s日线突破股票列表" % target_date)

    # 准备进度条
    bar = 0;
    bar_total = len(stocklist)
    pbar = progressbar.ProgressBar(max_value= bar_total).start()

    for stock in stocklist:
        pbar.update(bar)  # 更新进度条
        bar += 1

        query2 = "select * from '%s' order by date" %stock
        df = pd.read_sql(query2, con)
        df = df.set_index('date')

        # 若交易记录少于10条，跳过
        if len(df) < 10:
            continue
        # 若无法找到目标日的交易数据（停牌），跳过
        if target_date not in df.index:
            continue

        df.index = pd.to_datetime(df.index)
        df = df["2017-01-01":target_date]  # 只取2017年至目标日的记录

        close = df.close
        mean5 = close.rolling(window=5,center=False).mean()
        mean20 = close.rolling(window=20,center=False).mean()
        if mean5[-1]>mean20[-1]:
            if int(df.ix[-1,"volume"]) > int(df.ix[-2,"volume"])*2:
                sign = True
                for i in range(-2,-10,-1):
                    if mean5[i] > mean20[i]:
                        sign = False
                if sign:
                    #result_file.write(stock + ',')
                    result.append(stock)

    pbar.finish()
    log.write(log_file, "完成抓取%s日线突破股票列表，共获得%s只股票" % (target_date, len(result)))

    # 如果获取日期为现有记录的下一个交易日，则添加记录
    result_file = open('focus/mean_deal.csv', 'r')
    result_file_lines = result_file.readlines()
    result_file.close()
    if len(result_file_lines) != 0:  # 如果文件没有记录，直接加入记录
        last_recode_date = result_file_lines[-1].split(',')[0]
        print make_data.get_trade_dates(last_recode_date, n=1)
        print target_date
        # 获取从最晚记录日期到target_date的日期序列
        # 如果后者早于或等于前者，则直接返回结果，不更新记录文件
        # 如果后者晚于前者1天以上，则递归更新记录
        date_list = make_data.get_trade_dates(date_start=last_recode_date,date_end=target_date)
        if date_list == False or len(date_list) < 2:
            return result
        if len(date_list) > 2:
            get_mean_deal(date_list[-2])

    # 如果正好相差一天，则更新记录
    log.write(log_file, "更新记录文件")
    result_file = open('focus/mean_deal.csv', 'a+')
    result_file.write(target_date + ',' + ','.join(result) + '\n')
    result_file.close()
    return result
