import pandas as pd

#to read on your computer, change the address#
jd=pd.read_csv("C:/Users/drh/Desktop/XFC/jd.csv")
baba=pd.read_csv("C:/Users/drh/Desktop/XFC/baba.csv")
ttwo=pd.read_csv("C:/Users/drh/Desktop/XFC/ttwo.csv")

#list of companies in the portfolio#
portfolio=[jd.loc[:,lambda df : ["Date","Close"]],baba.loc[:,lambda df : ["Date","Close"]],ttwo.loc[:,lambda df : ["Date","Close"]]]

#creating a panda dataframe with date, and close prices of the different assets#
n=len(portfolio)
daily_return=portfolio[0]
for i in range(n-1):
    daily_return=pd.merge(daily_return,portfolio[i+1],on="Date")

#from prices to returns
daily_return=daily_return.iloc[:,1:n+1].pct_change(1)
 
#returns observation period
T=daily_return.shape[0]-1 
 
#demean returns then divide them by cross-sectional vol and sample vol to normalize#
daily_return=daily_return.sub(daily_return.mean(),axis=1)
daily_return=daily_return.div(daily_return.std(axis=1),axis=0)
daily_return=daily_return.div(daily_return.std(axis=0),axis=1)

#Naive estimator that we're going to clean#
estimator=(1/T)*daily_return.dot(daily_return.transpose())
    
    
