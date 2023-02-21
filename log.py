import numpy as np
import pandas as pd
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import seaborn as sn
import os
from datetime import date


#--------------V0 get base code
os.chdir(r'/')

#data=pd.read_csv('paper-trading-account-history-2023-02-21T22_05_24.143Z.csv')
data=pd.read_csv('paper-trading-account-history-2023-02-10T19_11_54.761Z.csv')


data=data.rename(columns=lambda x: x.strip())

data=data.drop(['Balance Before', 'Balance After'], axis= 1)

try:
    data.rename({'Profit': 'P&L'}, axis=1, inplace=True)
except:
    pass 

if data['P&L'].dtype!=np.float:
   data['P&L']=data['P&L'].str.replace(" ", "") 
   data['P&L']=data['P&L'].str.replace(" ", "") 
   data['P&L']=data['P&L'].apply(lambda x: float (x))
data=data[data['P&L']!=-1]


try:
    data['Time']=pd.to_datetime(data['Time'], format='%m/%d/%Y %H:%M')
    data['date']=data['Time'].dt.date
    data['time']=data['Time'].dt.time
except:
    pass
try:
    data['Time']=pd.to_datetime(data['Time'], format='%m/%d/%y %H:%M')
    data['date']=data['Time'].dt.date
    data['time']=data['Time'].dt.time
except:
    pass
try:
    data['Time']=pd.to_datetime(data['Time'], format='%Y-%m-%d %H:%M:%S')
    data['date']=data['Time'].dt.date
    data['time']=data['Time'].dt.time
except:
    pass


data['Action']=data['Action'].str.replace(',' ,'')

p=data['Action'].str.split(' ', expand=True)
q=p[[1,5,8,10,16,21]]

data=data.join(q)

data.rename({'P&L':'pnl', 1:'type', 5:'ticker', 8:'price1', 10:'shares', 16:'price2', 21:'contracts_in' }, axis=1, inplace=True)

data=data.drop(['Action'], axis=1)
data['ticker']=data['ticker'].str.replace('CME_MINI:', '')
data['ticker']=data['ticker'].str.replace('1!', '')
data['ticker']=data['ticker'].str.replace('NASDAQ:', '')
data['ticker']=data['ticker'].str.replace('AMEX:', '')

data['price1']=data['price1'].apply(lambda x: x.strip())
data['price1']=data['price1'].apply(lambda x: float(x))

data['price2']=data['price2'].apply(lambda x: x.strip())
data['shares']=data['shares'].apply(lambda x: float(x))
data['contracts_in']=data['contracts_in'].apply(lambda x: float(x))

data['cnt']=1
data.loc[data['time']<datetime.time(9, 30, 0), 'time_ind']='a.pm'
data.loc[(data['time']>=datetime.time(9, 30, 0)) & (data['time']<datetime.time(10, 0, 0)), 'time_ind']='b.open'    
data.loc[(data['time']>=datetime.time (10, 0, 0)) & (data['time']<datetime.time(11, 0, 0)), 'time_ind']='c.10-11' 
data.loc[(data['time']>=datetime.time (11, 0, 0)) & (data['time']<datetime.time(13, 0, 0)), 'time_ind']='d.11-1' 
data.loc[(data['time']>=datetime.time (13, 0, 0)) & (data['time']<datetime.time(15, 30, 0)), 'time_ind']='e.afternoon' 
data.loc[(data['time']>=datetime.time (15, 30, 0)) & (data['time']<datetime.time(16, 00, 0)), 'time_ind']='f.close' 
data.loc[data['time']>datetime.time(16, 0, 0), 'time_ind']='e.am'

data['day_of_week']=data['Time'].dt.day_name()


#-----------------------------------V1 - loop over csv files

columnss=['Time', 'pnl', 'date', 'time', 'type', 'ticker', 'price1', 'shares', 'price2', 'contracts_in', 'cnt', 'time_ind', 'day_of_week']
base=pd.DataFrame(columns=columnss)

os.chdir(r'//')
files=os.listdir()

files=list(filter(lambda x: '.csv' in x, files))

for file in files:
    
    data=pd.read_csv(file)
    
    data=data.rename(columns=lambda x: x.strip())
    
    data=data.drop(['Balance Before', 'Balance After'], axis= 1)
    
    try:
        data.rename({'Profit': 'P&L'}, axis=1, inplace=True)
    except:
        pass 
    
    if data['P&L'].dtype!=np.float:
       data['P&L']=data['P&L'].str.replace(" ", "") 
       data['P&L']=data['P&L'].str.replace(" ", "") 
       data['P&L']=data['P&L'].apply(lambda x: float (x))
    data=data[data['P&L']!=-1]
    
    
    try:
        data['Time']=pd.to_datetime(data['Time'], format='%m/%d/%Y %H:%M')
        data['date']=data['Time'].dt.date
        data['time']=data['Time'].dt.time
    except:
        pass
    try:
        data['Time']=pd.to_datetime(data['Time'], format='%m/%d/%y %H:%M')
        data['date']=data['Time'].dt.date
        data['time']=data['Time'].dt.time
    except:
        pass
    try:
        data['Time']=pd.to_datetime(data['Time'], format='%Y-%m-%d %H:%M:%S')
        data['date']=data['Time'].dt.date
        data['time']=data['Time'].dt.time
    except:
        pass
    
    
    data['Action']=data['Action'].str.replace(',' ,'')
    
    p=data['Action'].str.split(' ', expand=True)
    q=p[[1,5,8,10,16,21]]
    
    data=data.join(q)
    
    data.rename({'P&L':'pnl', 1:'type', 5:'ticker', 8:'price1', 10:'shares', 16:'price2', 21:'contracts_in' }, axis=1, inplace=True)
    
    data=data.drop(['Action'], axis=1)
    data['ticker']=data['ticker'].str.replace('CME_MINI:', '')
    data['ticker']=data['ticker'].str.replace('1!', '')
    data['ticker']=data['ticker'].str.replace('NASDAQ:', '')
    data['ticker']=data['ticker'].str.replace('AMEX:', '')
    
    data['price1']=data['price1'].apply(lambda x: x.strip())
    data['price1']=data['price1'].apply(lambda x: float(x))
    
    data['price2']=data['price2'].apply(lambda x: x.strip())
    data['shares']=data['shares'].apply(lambda x: float(x))
    data['contracts_in']=data['contracts_in'].apply(lambda x: float(x))
    
    data['cnt']=1
    data.loc[data['time']<datetime.time(9, 30, 0), 'time_ind']='a.pm'
    data.loc[(data['time']>=datetime.time(9, 30, 0)) & (data['time']<datetime.time(10, 0, 0)), 'time_ind']='b.open'    
    data.loc[(data['time']>=datetime.time (10, 0, 0)) & (data['time']<datetime.time(11, 0, 0)), 'time_ind']='c.10-11' 
    data.loc[(data['time']>=datetime.time (11, 0, 0)) & (data['time']<datetime.time(13, 0, 0)), 'time_ind']='d.11-1' 
    data.loc[(data['time']>=datetime.time (13, 0, 0)) & (data['time']<datetime.time(15, 30, 0)), 'time_ind']='e.afternoon' 
    data.loc[(data['time']>=datetime.time (15, 30, 0)) & (data['time']<datetime.time(16, 00, 0)), 'time_ind']='f.close' 
    data.loc[data['time']>datetime.time(16, 0, 0), 'time_ind']='e.am'
    
    data['day_of_week']=data['Time'].dt.day_name()
        
    base=base.append(data)

base=base.drop_duplicates()

base = base.sort_values(by=['Time'], ascending=True)

base['numid']=np.arange(len(base))

base.index=base.numid


os.chdir(r'/')
today = date.today()
base.to_excel('paper_log_{0}.xlsx'.format(today))







