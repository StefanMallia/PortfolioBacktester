from datetime import date, datetime
from urllib import request
import pandas as pd

class Security:
    def getHistory(ticker, startDate, endDate):
        if (not isinstance(startDate, date) or not isinstance(endDate, date) ):
            raise Exception("Dates should be inputted as date object from datetime")



        
        if (endDate == None):
            endDate = date.today()#datetime.strftime(date.today(), "%d/%m/%Y")

        endpoint= "http://real-chart.finance.yahoo.com/table.csv?s="+ ticker + \
                  "&a=" + str(startDate.month-1) + \
                  "&b=" + str(startDate.day) + \
                  "&c=" + str(startDate.year) + \
                  "&d=" + str(endDate.month-1) + \
                  "&e=" + str(endDate.day) + \
                  "&f=" + str(endDate.year) + \
                  "&g=d&ignore=.csv"


        req = request.Request(endpoint)
        response = request.urlopen(req)
        csv_response = pd.read_csv(response, sep=',')
        csv_response['Date'] =[datetime.strptime(csv_response['Date'][x], "%Y-%m-%d").date() for x in range(len(csv_response['Date']))]
        csv_response.set_index('Date', inplace = True)
        csv_response.rename(columns={'Adj Close': ticker}, inplace=True)
        return csv_response[[ticker]]




