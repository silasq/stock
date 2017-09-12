import tushare as ts
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt



con = sqlite3.connect('History.db')
query1 = "select name from sqlite_master where type='table' order by name"
stocklist = pd.read_sql(query1, con).name

engine = create_engine('sqlite:///History.db', echo = False)

count = 0

query2 = "select * from sz002594 order by date"
df = pd.read_sql(query2, con)
df = df.set_index('date')
df.index = pd.to_datetime(df.index)
close = df.close
open = df.open
clop = close - open
ret=close/close.shift(1)-1

mean5 = pd.rolling_mean(close,5)
mean20 = pd.rolling_mean(close,20)

print mean5[-1],mean20[-1]

#plt.plot(df.open)
#plt.show()