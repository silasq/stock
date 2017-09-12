# coding=utf-8

import log
import datetime
import pandas as pd
import index

"""
放置数据整理方法
返回sh或sz开头的股票代码，无法识别则反悔False
"""
def num2stock(num, log_file):
    # 对于非字符串，先转换为字符串格式
    if not isinstance(num,str):
        num = str(num)

    # 60开头为沪市，00、30开头为深市
    if num.startswith("60"):
        code = "sh" + num
        return code
    elif num.startswith("00") or num.startswith("30"):
        code = "sz" + num
        return code
    else:
    # 其余报错并记录日志
        log.write(log_file,"error : unknow code :" + num)
        return False


# """
# 获得上一个交易日日期
# 周末获得周五日期，交易日15点前获得前一天日期，15点后获得当日日期
# """
# def last_trade_date():
#     today = datetime.datetime.now()
#     if today.weekday() == 5:
#         last_trade_date = str(today - datetime.timedelta(days=1))[:10]
#     elif today.weekday() == 6:
#         last_trade_date = str(today - datetime.timedelta(days=2))[:10]
#     else:
#         if datetime.datetime.now().hour < 15:
#             last_trade_date = str(today - datetime.timedelta(days=1))[:10]
#         else:
#             last_trade_date = str(today)[:10]
#
#     return last_trade_date


# 获得前n个交易日日期
# 需要先刷新index_sh
def last_trade_date(dates = 1):
    #index.refresh_all()  # 刷新所有指数行情
    df = pd.read_csv("./index/index_sz", header=0)  # 加载上证指数数据

    result = []
    for i in range(0,dates):
        result.append(df.at[i,"date"])

    return result


# 根据指定日期，获取前（后）n个交易日的日期
# n:正数为后n个交易日，负数为前n个交易日，默认为1
def next_trade_date(date, n=1):
    df = pd.read_csv("./index/index_sz", header=0,)  # 加载上证指数数据
    date_list = df.date.tolist()

    # 若指定交易日不存在，返回False
    if date not in date_list:
        return False

    # 若计算天数超出范围，返回False
    target_date_index = date_list.index(date) - n
    if target_date_index < 0 or target_date_index > len(date_list) - 1:
        return False

    return date_list[target_date_index]


'''
通过stock_basics.csv文件获得股票代码对应股票名称
'''
def get_stock_name(code):
    df = pd.read_csv("stock_basics.csv", header=0,dtype={'code':str})
    df = df.set_index('code')
    return df.loc[code,'name']
