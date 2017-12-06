import pandas as pd
import numpy as np

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
daily_return=daily_return.iloc[:,1:n+1].pct_change(1).iloc[1:,:]
 
#returns observation period
T=daily_return.shape[0]
 
#demean returns then divide them by cross-sectional vol and sample vol to normalize#
daily_return=daily_return.sub(daily_return.mean(),axis=1)
daily_return=daily_return.div(daily_return.std(axis=1),axis=0)
daily_return=daily_return.div(daily_return.std(axis=0),axis=1)

#naive estimator that we're going to clean#
estimator=(1/T)*daily_return.transpose().dot(daily_return)

#computing the RIE's eigenvalues before correction
eigen=np.linalg.eigh(estimator)
eigen_val=eigen[0]
eigen_vec=eigen[1]

eta=1/(np.sqrt(n))
q=n/T

z=np.arange(len(eigen_val),dtype=complex)
for i in range(len(eigen_val)):
    z[i]=complex(eigen_val[i],-eta)

def s(comp,k):
    res=0
    for j in range(n):
        if j!=k:
            res=res+1/(comp-eigen_val[j])
    return (1/n)*res


new_eigen_val=np.arange(len(eigen_val), dtype=float)
for k in range(n):
    new_eigen_val[k]=eigen_val[k]/(abs(1-q+q*z[k]*s(z[k],k)))**2

#computing the correction factor gamma(k)
lambda_N=np.amin(eigen_val)
lambda_plus=lambda_N*((1+np.sqrt(q))/(1-np.sqrt(q)))**2
sigma_2=lambda_N/((1-np.sqrt(q))**2)

def g(comp):
    return (comp+sigma_2*(q-1)-np.sqrt(comp-lambda_N)*np.sqrt(comp-lambda_plus))/(2*q*comp*sigma_2)

gamma=np.arange(n, dtype=float)
for k in range(n):
    gamma[k]=sigma_2*(abs(1-q+q*z[k]*g(z[k]))**2)/eigen_val[k]

#computing the corrected eigen values
corrected_eigen_val=np.arange(len(eigen_val), dtype=float)
for k in range(n):
    if gamma[k]>1:
        corrected_eigen_val[k]=gamma[k]*new_eigen_val[k]
    else:
        corrected_eigen_val[k]=new_eigen_val[k]


#Clean Correlation matrix C
C=np.zeros((n,n))
for k in range(n):
    C=C+corrected_eigen_val[k]*np.dot(eigen_vec[:,k][:,np.newaxis],eigen_vec[:,k][np.newaxis,:])
C=pd.DataFrame(data=C)
    
    
