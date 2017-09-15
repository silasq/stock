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
    df = pd.read_csv("index/index_sz", header=0)  # 加载上证指数数据

    result = []
    for i in range(0,dates):
        result.append(df.at[i,"date"])

    return result


# 根据指定日期，获取前（后）n个交易日的日期序列，按时间递增排列
# 若给出date_end日期，则返回从date_start到date_end的日期序列
# 若没有给出date_end日期，则根据n取值
# n:正数为后n个交易日，负数为前n个交易日
# 默认为0，即验证所给日期是否为交易日，不是则返回False
def get_trade_dates(date_start, date_end='', n=0):
    df = pd.read_csv("index/index_sz", header=0,)  # 加载上证指数数据
    date_list = df.date.tolist()
    date_list.reverse()

    # 若起始日期不是交易日，返回False
    if date_start not in date_list:
        return False
    date_start_index = date_list.index(date_start)

    # 若给出date_end日期，则返回从date_start到date_end的日期序列
    if date_end != '':
        # 若结束日期不是交易日，返回False
        if date_end not in date_list:
            return False
        if date_start == date_end:
            return [date_start]
        date_end_index = date_list.index(date_end)
        # 如果结束日期早于开始日期，返回False
        if date_end_index < date_start_index:
            return False
        else:
            return date_list[date_start_index:date_end_index + 1]

    # 如果没给出date_end值，则根据n取值
    target_date_index = date_start_index + n
    if target_date_index < 0 or target_date_index + 1 > len(date_list):  # 若计算天数超出范围，返回False
        return False
    if n > 0:
        return date_list[date_start_index:target_date_index + 1]
    elif n < 0:
        return date_list[target_date_index:date_start_index + 1]
    else:
        return date_list[target_date_index]


# 通过stock_basics.csv文件获得股票代码对应股票名称
def get_stock_name(code):
    df = pd.read_csv("database/stock_basics.csv", header=0,dtype={'code':str})
    df = df.set_index('code')
    return df.loc[code, 'name']
