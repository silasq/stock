# coding=utf-8

import tushare as ts
import log
import os


def refresh_all():
    log_file = open("log/index.log", 'a+')

    log.write(log_file,"refresh all index data start!")

    # 若果database目录不存在，则新建
    if not os.path.exists('index'):
        os.makedirs('index')

    # 更新指数：上证指数，深成指数，创业板，中小板，上证50，沪深300
    index_list = ['sh', 'sz', 'cyb', 'zxb', 'sz50', 'hs300']
    for i in index_list:
        df = ts.get_hist_data(i)
        df.to_csv('./index/index_%s' % i)
    log.write(log_file, "refresh all index data finish!")
