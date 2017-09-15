#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import get_all_stock
import get_hist
import index
from analyze import *
import focus
import send_mail

if __name__ == "__main__":
    if not os.path.exists('log'):
        os.makedirs('log')

    index.refresh_all() # 更新指数信息
    get_all_stock.get()  # 更新股票数据库，对新增股票代码新建数据表
    get_hist.refresh_all()  # 更新股票数据

    mean_deal.get() # 更新关注列表
    html_file = focus.trace_focus("mean_deal.csv")
    html_text = open(html_file).readlines()
    send_mail.send_mail(''.join(html_text))


