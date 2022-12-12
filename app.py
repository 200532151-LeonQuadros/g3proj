from flask import Flask, request, render_template, jsonify
import pymongo
from bson import json_util
import pandas as pd

import json
from datetime import date, timedelta

import requests
import time

app=Flask(__name__)

#Import data from MongoDB
myclient = pymongo.MongoClient("mongodb+srv://Hoanglong_Pham:Long1989@cluster0.j3atpvd.mongodb.net/?retryWrites=true&w=majority")

# # Add the meta data into stock price information
# def meta_stock(info, symbol): 
#     if symbol in nasdaq_list:
#         exchange = 'Nasdaq 100'
#     elif symbol in dowjones_list:
#         exchange = 'Dow Jones'
#     else:
#         exchange = 'Other exchange'
#     company = yf.Ticker(symbol)
#     name = company.info['shortName']    
#     meta = {'Meta data':{'Fullname': name, 'Symbol': symbol, 'Exchange': exchange},'Time Series': {}}
#     meta['Time Series'] = info
#     return meta

# # Add the meta data into stock exchange market price information
# def meta_exchange(info, symbol):    
#     exchange = yf.Ticker(symbol)
#     name = exchange.info['shortName']
#     abb = exchange.info['exchange']
#     time_zone = exchange.info['exchangeTimezoneName']   
#     meta = {'Meta data':{'Fullname': name, 'Symbol': abb, 'Time zone': time_zone},'Time Series': {}}
#     meta['Time Series'] = info
#     return meta

# #Generate price information for specific stock based on symbol and specificed day range
# def stock_info(symbol, day_range):
#     from pandas_datareader import data
#     end_date = date.today()
#     if day_range == 'today':
#         start_date = end_date
#     elif day_range == '1 week':
#         start_date = end_date - timedelta(days=7)
#     elif day_range == '1 month':
#         start_date = end_date - timedelta(days=30)
#     elif day_range == '1 year':
#         start_date = end_date - timedelta(days=365)
#     elif day_range == '5 year':
#         start_date = end_date - timedelta(days=1825)
#     elif day_range == '10 year':
#         start_date = end_date - timedelta(days=3650)
#     elif day_range == 'All':
#         start_date = '2010-01-01'
#     data_source='yahoo'
#     df_stock = data.DataReader(symbol, data_source, start_date, end_date)
#     df_stock=df_stock.to_json(date_format = 'iso', orient='index')
#     info = json.loads(df_stock)
#     return info

# #Generate complete information of each stock
# def stock_price(symbol):
#     info = stock_info(symbol, 'All')
#     meta = meta_stock(info, symbol)
#     return meta

# #Generate complete information of exchange market
# def exchange_price(symbol):
#     info = stock_info(symbol, 'All')
#     meta = meta_exchange(info, symbol)
#     return meta

# #Generate complete informtion stock price for today date
# def today_stock():
#     today_stock = {}
#     i = 1
#     for symbol in nasdaq_list:
#         info = stock_info(symbol, 'today')
#         today_stock[symbol] = info
#     return today_stock

# while True:
#     #Generate the list of stocks in Dow Jones exchange market:
#     dowjones_link = 'https://www.slickcharts.com/dowjones'
#     r1 = requests.get(dowjones_link, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
#     dj_data = pd.read_html(r1.text)[0]
#     df1 = pd.DataFrame(dj_data)
#     df1 = df1.to_json(date_format = 'iso', orient='index')
#     dowjones = json.loads(df1)
#     dowjones_list=[]
#     for i in dowjones:
#         dowjones_list.append(dowjones[i]['Symbol'])
#     print('Completed downloading Dow Jones stock list')

#     #Generate the list of stocks in Nasdaq 100 exchange market:
#     nasdaq_link = 'https://www.slickcharts.com/nasdaq100'
#     r2 = requests.get(nasdaq_link, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
#     nd_data = pd.read_html(r2.text)[0]
#     df2 = pd.DataFrame(nd_data)
#     df2 = df2.to_json(date_format = 'iso', orient='index')
#     nasdaq = json.loads(df2)
#     nasdaq_list=[]
#     for j in nasdaq:
#         nasdaq_list.append(nasdaq[j]['Symbol'])
#     print('Completed downloading Nasdaq stock list')
        
#     #Upload information of stocks into MongoDB
#     myclient = pymongo.MongoClient("mongodb+srv://Hoanglong_Pham:Long1989@cluster0.j3atpvd.mongodb.net/?retryWrites=true&w=majority")

#     #Upload information of each stock from Nasdaq100
#     mydb1 = myclient["Nasdaq"]
#     collist1 = mydb1.list_collection_names()
#     for symbol in nasdaq_list:
#         value = stock_price(symbol)
#         mycol1 = mydb1[symbol]
#         if symbol in collist1:
#             mycol1.drop()
#             mycol1.insert_one(value)
#             print('Updated ' + symbol)
#         else:
#             mycol1.insert_one(value)
#             print('Created ' + symbol)

#     #Upload information of each stock from Dow Jones
#     mydb2 = myclient["DowJones"]
#     collist2 = mydb2.list_collection_names()
#     for symbol in dowjones_list:
#         value = stock_price(symbol)
#         mycol2 = mydb2[symbol]
        
#         if symbol in collist2:
#             mycol2.drop()
#             mycol2.insert_one(value)
#             print('Updated ' + symbol)
#         else:
#             mycol2.insert_one(value)
#             print('Created ' + symbol)

#     #Upload general stock of Nasdaq100 and Dow Jones
#     mydb = myclient["ExchangeMarket"]
#     nasdaq_info = exchange_price('%5ENDX')
#     dowjones_info = exchange_price('%5EDJI')
#     mycol3 = mydb['Nasdaq100']
#     mycol4 = mydb['Dow Jones']
#     collist3 = mydb.list_collection_names()
#     if 'Nasdaq100' in collist3:
#         mycol3.drop()
#         mycol3.insert_one(nasdaq_info)
#         print('Updated ' + symbol)
#     else:
#         mycol3.insert_one(nasdaq_info)
#         print('Created ' + symbol)
        
#     if 'Dow Jones' in collist3:
#         mycol4.drop()
#         mycol4.insert_one(dowjones_info)
#         print('Updated ' + symbol)
#     else:
#         mycol4.insert_one(dowjones_info)
#         print('Created ' + symbol)
#     time.sleep(86400)

def present_exchange(exchange_name, day_range):
  mydb = myclient['ExchangeMarket']
  mycol = mydb[exchange_name]
  mydoc = mycol.find_one({})
  data_display = mydoc['Time Series']
  sanitized = json.loads(json_util.dumps(data_display))
  df = pd.DataFrame(sanitized).iloc[:, ::-1].T
  df.reset_index(inplace=True)
  df.rename({'index': 'Date'}, axis=1, inplace=True)
  val = df.iloc[0:day_range,:5].to_json(orient="values")
  return val


# For your project you would want to manipulate this data further here


#small change
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/mongojson')
def mongodbjson():
	return render_template('mongojson.html', json=json) 

@app.route('/piechart')
def piechart():

  # Created this dictionary called data
  
  #Get the mongoDB data here, and then pass it like so to the html

  data = { "Task" : "Hours per Day",  "Work" :3, "Eat" : 6, "Commute" : 2, "Watch TV" : 6}
  print(type(data))
  print(data)
  mynumber =5

  return render_template('pie-chart.html', data=data, mynumber=mynumber) 

@app.route('/data')
def data():
  mydb = myclient['ExchangeMarket']
  mycol = mydb['Nasdaq100']
  mydoc = mycol.find_one({})
  data_display = mydoc['Time Series']
  sanitized = json.loads(json_util.dumps(data_display))
  df = pd.DataFrame(sanitized).iloc[:, ::-1].T
  df.reset_index(inplace=True)
  df.rename({'index': 'Date'}, axis=1, inplace=True)
  n = 10
  val = df.iloc[0:n,0:5].to_json(orient = 'values')
  return render_template('mongojson.html', json=val)

@app.route('/candlestick')
def candlestick():
  # mydb = myclient['ExchangeMarket']
  # mycol = mydb['Nasdaq100']
  # mydoc = mycol.find_one({})
  # data_display = mydoc['Time Series']
  # sanitized = json.loads(json_util.dumps(data_display))
  # df = pd.DataFrame(sanitized).iloc[:, ::-1].T
  # df.reset_index(inplace=True)
  # df.rename({'index': 'Date'}, axis=1, inplace=True)
  # n = 10
  # val = json.loads(df.iloc[0:n,0:5].T.to_json(orient = 'values'))
  return render_template('candle-stick.html')

if __name__ == "__main__":
  app.run()