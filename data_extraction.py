import pandas_datareader.data as web
import datetime
start=datetime.datetime(1990,1,1) 
end=datetime.datetime(2017,11,20)

#Open/High/Low/Close/Volume tous les jours#
jd = web.DataReader("jd", 'yahoo', start, end)
baba= web.DataReader("baba", 'yahoo', start, end)
ttwo= web.DataReader("ttwo", 'yahoo', start, end)

a=jd.isnull().values.any() #verifie qu'il n'y aucune valeur NaN dans jd (de même pour baba et ttwo)#

