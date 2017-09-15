# coding=utf-8

import sqlite3
import pandas as pd
import make_data
import log
import progressbar
import os


#
#
def get(target_date=''):
    log_file = open("log/analyze.log", 'a+')

    # 设置默认值，无法设为默认参数因为第一次运行会报错
    if target_date == '':
        target_date = make_data.last_trade_date()[0]
    else:
        if not make_data.get_trade_dates(date_start=target_date):
            log.write(log_file, '%s 非交易日或超出交易记录范围！' % target_date)
            return False

    con = sqlite3.connect('database/History.db')
    query1 = "select name from sqlite_master where type='table' order by name"
    stocklist = pd.read_sql(query1, con).name
    result = []  # 保存抓取股票列表

    log.write(log_file, "开始抓取%s清晨之星股票列表" % target_date)

    # 准备进度条
    bar = 0;
    bar_total = len(stocklist)
    pbar = progressbar.ProgressBar(max_value=bar_total).start()

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
        # 只取2017年至目标日的记录
        df.index = pd.to_datetime(df.index)
        df = df["2017-01-01":target_date]

        if len(df) < 10:
            continue

        price_close = df.close
        price_open = df.open
        clop = price_close - price_open
        ret=price_close/price_close.shift(1)-1
        clop_wav = abs(clop.describe()["25%"]) * 4

        if all([clop[-3] < clop_wav*(-1), abs(clop[-2]) < clop_wav/2 , clop[-1] > clop_wav/2,abs(clop[-1] > abs(clop[-3] * 0.5))]):
            if all([price_open[-2] < price_open[-1], price_open[-2] < price_close[-3], price_close[-2] < price_open[-1],price_close[-2] < price_close[-3]]):
                if all([ret[-4] < 0, ret[-5] < 0]):
                    result.append(stock)

        # if all([clop[-2] < clop_wav * (-1), abs(clop[-1]) < clop_wav/2]):
        #     if all([price_open[-1] < price_close[-2], price_close[-1] < price_close[-2]]):
        #         if all([ret[-3] < 0, ret[-4] < 0]):
        #             print str(stock) + ":" + str(df.index[-2]) + " looks lisk!"

    pbar.finish()
    log.write(log_file, "完成抓取%s清晨之星股票列表，共获得%s只股票" % (target_date, len(result)))

    # 如果记录文件不存在，则新建
    if not os.path.exists('focus/sunrise.csv'):
        os.mknod('focus/sunrise.csv')

    # 如果获取日期为现有记录的下一个交易日，则添加记录
    result_file = open('focus/sunrise.csv', 'r')
    result_file_lines = result_file.readlines()
    result_file.close()
    if len(result_file_lines) != 0:  # 如果文件没有记录，直接加入记录
        last_recode_date = result_file_lines[-1].split(',')[0].strip()
        # 获取从最晚记录日期到target_date的日期序列
        # 如果后者早于或等于前者，则直接返回结果，不更新记录文件
        # 如果后者晚于前者1天以上，则递归更新记录
        date_list = make_data.get_trade_dates(date_start=last_recode_date,date_end=target_date)
        if date_list == False or len(date_list) < 2:
            return result
        if len(date_list) > 2:
            get(date_list[-2])

    # 如果正好相差一天，则更新记录
    log.write(log_file, "更新记录文件")
    result_file = open('focus/sunrise.csv', 'a+')
    # 如果获取股票数为0，则只记录日期
    if len(result) == 0:
        result_file.write(target_date + '\n')
    else:
        result_file.write(target_date + ',' + ','.join(result) + '\n')
    result_file.close()
    return result
