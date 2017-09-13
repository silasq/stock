import tushare as ts
from sqlalchemy import create_engine
import sqlite3
import pandas as pd

def get():
    con = sqlite3.connect('database/History.db')
    query1 = "select name from sqlite_master where type='table' order by name"
    stocklist = pd.read_sql(query1, con).name

    engine = create_engine('sqlite:///History.db', echo = False)

    count = 0
    for stock in stocklist:
        query2 = "select * from '%s' order by date" %stock
        df = pd.read_sql(query2, con)
        df = df.set_index('date')
        df.index = pd.to_datetime(df.index)
        df = df["2017":"2017"]

        if len(df) < 10:
            continue

        close = df.close
        open = df.open
        clop = close - open
        ret=close/close.shift(1)-1
        clop_wav = abs(clop.describe()["25%"]) * 4


        if all([clop[-3] < clop_wav*(-1), abs(clop[-2]) < clop_wav/2 , clop[-1] > clop_wav/2,abs(clop[-1] > abs(clop[-3] * 0.5))]):
            if all([open[-2] < open[-1], open[-2] < close[-3], close[-2] < open[-1],close[-2] < close[-3]]):
                if all([ret[-4] < 0, ret[-5] < 0]):
                    print str(stock) + ":" + str(df.index[-3])

        if all([clop[-2] < clop_wav * (-1), abs(clop[-1]) < clop_wav/2]):
            if all([open[-1] < close[-2], close[-1] < close[-2]]):
                if all([ret[-3] < 0, ret[-4] < 0]):
                    print str(stock) + ":" + str(df.index[-2]) + " looks lisk!"
