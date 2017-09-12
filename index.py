# coding=utf-8

import tushare as ts
import log

log_file = open("log/index.log", 'a+')


def refresh_all():
    log.write(log_file,"refresh all index data start!")
    index_list = ['sh', 'sz', 'cyb', 'zxb', 'sz50', 'hs300']
    for i in index_list:
        df = ts.get_hist_data(i)
        df.to_csv('./index/index_%s' % i)
    log.write(log_file, "refresh all index data finish!")
