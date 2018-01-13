import pandas as pd
import pandas_datareader.data as web
import datetime
start=datetime.datetime(1990,1,1) 
end=datetime.date.today()

#Open/High/Low/Close/Volume tous les jours#
jd = web.DataReader("jd", 'yahoo', start, end)
baba= web.DataReader("baba", 'yahoo', start, end)
ttwo= web.DataReader("ttwo", 'yahoo', start, end)


jd.to_csv("C:/Users/drh/Desktop/XFC/jd.csv",index=False)
baba.to_csv("C:/Users/drh/Desktop/XFC/baba.csv",index=False)
ttwo.to_csv("C:/Users/drh/Desktop/XFC/ttwo.csv",index=False)

