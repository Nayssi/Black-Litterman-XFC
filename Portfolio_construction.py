import pandas as pd
import numpy as np
from scipy.optimize import minimize

#Importation des données
corr_matrix=pd.read_csv("C:/Users/drh/Desktop/XFC/corr_matrix.csv")
daily_ret=pd.read_csv("C:/Users/drh/Desktop/XFC/daily_return.csv")

#Etat initial du portefeuille
N=daily_ret.shape[1] 
w_initial=np.zeros(N)
cash=80000

#from correlation matrix to covariance matrix 
daily_std=daily_ret.std()
cov_matrix=corr_matrix.copy()
for i in range(N):
    for j in range(N):
        cov_matrix.iloc[i][j]=cov_matrix.iloc[i][j]*daily_std[i]*daily_std[j]

#Paramètres de l'optimisation
lambda_c=0.1

#Bounds (pour que les poids soient toujours positifs car long-only)
bnds=[]
for i in range(N):
    bnds.append((0,None))

#Contrainte 1 pour minimisation de la variance: 
cons1=({'type':'eq','fun': lambda w: np.sum(w)-1})
    
#Trouver la variance minimale et définition de la variance du portfeuille (1,5*var_min)
def portfolio_var(w):
    return w.dot(cov_matrix.dot(w.transpose()))
w_0=minimize(portfolio_var,w_initial,constraints=cons1, bounds=bnds).x
var=1.5*portfolio_var(w_0)

#fonction de calcul du cout du rebalancement de portefeuille !!!A FAIRE!!!
def cout(w_initial,w_final):
    return -1

#Contrainte 2 pour la maximisation de return-coût (contrainte sur le risque et sur la somme des poids)
cons2=({'type':'ineq','fun': lambda w: var-w.dot(cov_matrix.dot(w.transpose()))},{'type':'eq','fun': lambda w: np.sum(w)-1})

#fonction à optimiser
def objective_function(w_final):
    return (-1)*(w_final.dot(daily_ret.mean())-lambda_c*cout(w_initial,w_final))

#poids final
w_final=minimize(objective_function,w_0,constraints=cons2, bounds=bnds).x



    
    


