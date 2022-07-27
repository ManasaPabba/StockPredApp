import time
import psycopg2
import pandas as pd
#import matplotlib.pyplot as plt
import io
import numpy as np
from datetime import datetime
from datetime import date, timedelta
from sqlalchemy import create_engine
import yfinance as yf
import streamlit as st
#from fbprophet import Prophet
#from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
#from pyngrok import ngrok

database = 'postgres'
user = 'demo'
password = '00'
host = 'db'
conn_string = "host='%s' dbname='%s' user='%s' password='%s'" %(host, database, user, password)
engine = create_engine('postgresql' + '://' + user + ':' + password + '@' + host + '/' + database)

# Some utilitiy functions
def rmse(y, y_h):
  return np.sqrt(np.mean(np.square(y_h - y)))


def r2(y, y_h, ave = None):
  if ave is None: ave = np.mean(y)
  ssa = np.square(y-y_h).sum()
  ssr = np.square(y-ave).sum()
  return 1-ssa/ssr

st.title('Stock Forecast App')

stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
symb = pd.read_csv('/home/app/stockList.csv', sep = ',')
symb=tuple(symb['stocks'])
selected_stock = st.selectbox('Select dataset for prediction', symb)
def load_data(ticker):
  df = yf.download(ticker, start=datetime.now() - timedelta(200), end=datetime.now())
  s=int(0.9*len(df))
  df[:s].to_csv('/home/app/stocksTrain.csv',header=False,sep="\t")
  df[s:].to_csv('/home/app/stocksTest.csv')
  df.to_csv('/home/app/totalData.csv',header=False,sep="\t")
  data_test = pd.read_csv('/home/app/stocksTest.csv', sep = ',')
  conn = psycopg2.connect(conn_string)
  cur = conn.cursor()
  cursor = conn.cursor()
  cur.execute(open("/home/app/load_data_Stock.sql", "r").read())
  cur.copy_from(open("/home/app/stocksTrain.csv"), "financial", null = "")
  cur.copy_from(open("/home/app/totalData.csv"), "financial2", null = "")
  cursor.execute("""select create_pindex('financial', 'time','{ "close","high","low"}','pindex1');""") #"volume","open","high", "low",  open and close have high corelation.!!(plot graph)
  cursor.execute("""select create_pindex('financial2', 'time','{        "close","high","low"}','pindex2');""")
  df2 = pd.read_sql_query("select * from  predict('financial','close','%s','%s','pindex1');"%(data_test.iloc[0]['Date'],data_test.iloc[-1]['Date']), conn)
  pred1 = pd.read_sql_query("select * from  predict('financial2','close','%s','%s','pindex2');"%(df.iloc[1].name ,datetime.now() +timedelta(60)), conn)
  conn.commit()
  conn.close()

  dfT2 = pd.DataFrame(data = pd.date_range(start=df.iloc[1].name ,end=datetime.now() +timedelta(60)).to_pydatetime(),columns=['date'])
  dfT = pd.DataFrame(data = pd.date_range(start=data_test.iloc[0]['Date'],end = data_test.iloc[-1]['Date']).to_pydatetime(),columns=['date'])
  dfT['date']=dfT['date'].apply(lambda x: x.date().strftime('%Y-%m-%d'))
  dfT=dfT[dfT['date'].isin(data_test['Date'])]
  df2=df2[df2.index.isin(dfT.index)]
  rsmev=rmse(df2['prediction'],data_test['Close'])
  print('RMSE = %.2f, $R^2$ = %.2f'%(rsmev, r2(data_test['Close'],df2['prediction'],)))
  st.subheader("test data results")
  data_test=data_test.reset_index()
  dfcopy=df.reset_index()

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=dfT['date'], y=df2['prediction'], name="predict"))
  fig.add_trace(go.Scatter(x=data_test['Date'], y=data_test['Close'], name="actualTestData"))
  st.plotly_chart(fig)
  st.text("root mean square error is %.2f" %(rsmev))

  st.subheader("prediction for next 60 days")

  fig1 = go.Figure()
  fig1.add_trace(go.Scatter(x=dfT2['date'], y=pred1['prediction'], name="pred(tspDB)"))
  fig1.add_trace(go.Scatter(x=dfcopy['Date'], y=df['Close'], name="actual"))
  st.plotly_chart(fig1)

  #return [df,dfT2,pred1]

data_load_state = st.text('Loading data...')
load_data(selected_stock)
data_load_state.text('')