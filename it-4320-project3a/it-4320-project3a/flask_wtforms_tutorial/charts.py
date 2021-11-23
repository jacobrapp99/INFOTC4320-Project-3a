'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def askCharts(chartType):
    
    chart = chartType
    chartNum = 0

    if chart == "1":
        chartNum = 1
    elif chart == "2":
        chartNum = 2
    else:
        chartNum = 0
        
    return chartNum
    

def askTimeSeries(stockSymbol, timeSeries):
    stock = stockSymbol
    
    
    series = timeSeries
    time = 0

    if series == "1":
        time = 1
    elif series == "2":
        time = 2
    elif series == "3":
        time = 3
    elif series == "4":
        time = 4
    else:
        time = 0
    
    apiKey = 'YY5C93IGQ19VMJXQ'
    if time == 1: 
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + stock + '&interval=60min&apikey=' + apiKey
    elif time == 2:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '&apikey=' + apiKey
    elif time == 3:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + stock + '&apikey=' + apiKey
    elif time == 4:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + stock + '&apikey=' + apiKey
    else:
        url = 0
           
    r = requests.get(url)
    data = r.json()
    return data, time

def generateGraph(stockSymbol, chartNum, series, data, sD, eD):
    
    format2 = "%Y-%m-%d %H:%M:%S"
    format = "%Y-%m-%d"
    high = []
    low =[]
    close =[]
    open = []
    dateList = []
    stock = stockSymbol
    chart = chartNum
    timeS = series
    sd = str(sD)
    ed = str(eD)
    datetime.strptime(sd, format)
    datetime.strptime(ed, format)
    dataList = data
    
    
    
    if timeS == 1:
        for date in dataList['Time Series (60min)']:
            datetime.strptime(date, format2)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Time Series (60min)'][date]['1. open'])
            high.append(dataList['Time Series (60min)'][date]['2. high'])
            low.append(dataList['Time Series (60min)'][date]['3. low'])
            close.append(dataList['Time Series (60min)'][date]['4. close'])

    if timeS == 2:
        for date in dataList['Time Series (Daily)']:
            datetime.strptime(date, format)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Time Series (Daily)'][date]['1. open'])
            high.append(dataList['Time Series (Daily)'][date]['2. high'])
            low.append(dataList['Time Series (Daily)'][date]['3. low'])
            close.append(dataList['Time Series (Daily)'][date]['4. close'])

    if timeS == 3:
        for date in dataList['Weekly Time Series']:
            datetime.strptime(date, format)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Weekly Time Series'][date]['1. open'])
            high.append(dataList['Weekly Time Series'][date]['2. high'])
            low.append(dataList['Weekly Time Series'][date]['3. low'])
            close.append(dataList['Weekly Time Series'][date]['4. close'])
            
    if timeS == 4:
        for date in dataList['Monthly Time Series']:
            datetime.strptime(date, format)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Monthly Time Series'][date]['1. open'])
            high.append(dataList['Monthly Time Series'][date]['2. high'])
            low.append(dataList['Monthly Time Series'][date]['3. low'])
            close.append(dataList['Monthly Time Series'][date]['4. close'])

    openFloat = [float(item) for item in open]
    highFloat = [float(item) for item in high]
    lowFloat = [float(item) for item in low]
    closeFloat = [float(item) for item in close]

    if chart == 1:
        bar = pygal.Bar(x_label_rotation=90)
        bar.title = stock
        bar.x_labels = map(str, dateList)
        bar.add('Open', openFloat)
        bar.add('High', highFloat)
        bar.add('Low', lowFloat)
        bar.add('Close', closeFloat)
        
        chart = bar.render_data_uri()

    if chart == 2:
        line = pygal.Line(x_label_rotation=90)
        line.title = stock
        line.x_labels = map(str, dateList)
        line.add('Open', openFloat)
        line.add('High', highFloat)
        line.add('Low', lowFloat)
        line.add('Close', closeFloat)
        
        chart = line.render_data_uri()

    return chart
    


def make_chart(symbol, chart_type, time_series, start_date, end_date):
    
    stockSymbol = symbol
    chartType = chart_type
    timeSeries = time_series
    startDate = str(start_date)
    endDate = str(end_date)

    chartNum = askCharts(chartType)
    data, series = askTimeSeries(stockSymbol, timeSeries)
    sD = convert_date(startDate)
    eD = convert_date(endDate)
    chart = generateGraph(stockSymbol, chartNum, series, data, sD, eD)       
    return chart 
        
        
