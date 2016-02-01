from urllib import request
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import json
import numpy as np
from SecurityClass import Security
from currencyPriceHistory import currencyPriceHistory , TradeInfo

class Portfolio:
    

    def __init__(self, cash, startDate, homeCurrency = 'EUR'):
        if (not isinstance(startDate, date)):
            raise Exception("Dates should be inputted as date object from datetime")
        self.tabulation = pd.DataFrame({homeCurrency: [cash]*((date.today()-startDate).days)}, index = [startDate + timedelta(days=x) for x in range(0, (date.today()-startDate).days)])

        currencies = ['EUR_USD', 'EUR_GBP', 'EUR_JPY', 'EUR_CHF', 'EUR_CAD', 'EUR_AUD', 'EUR_CZK', 'EUR_NZD']


        self.exchangeRates = pd.concat(
            [
                currencyPriceHistory(startDate, date.today(), TradeInfo('fxpractice.oanda.com',
                    '10cda01d38fecd780cfed36f0e258783-e3fa70cebcc468f9233534408d274020',
                    '3566119', currency, 'D'))
                for currency in currencies
            ]

            +
            
            [
                pd.DataFrame(1, index = [startDate + timedelta(days=x)
                                         for x in range(0, (date.today()-startDate).days)]
                             , columns = ["EUR_EUR"])
            ]

            , axis = 1, join='outer')


        
        print(self.exchangeRates)
        

        self.homeCurrency = homeCurrency

        
    def addSecurity(self, ticker, currency, startDate, amountShares, endDate = date.today()):
        if (not isinstance(startDate, date)or not isinstance(endDate, date) ):
            raise Exception("Dates should be inputted as date object from datetime")

        
        new_security = Security.getHistory(ticker, startDate, endDate)

        purchase_price = new_security[ticker][new_security.index.min()]*self.exchangeRates['EUR_'+currency][new_security.index.min()]*amountShares
        #using min() to find oldest possible date, yahoo does not return prices for weekends and holidays
        if (purchase_price > self.tabulation['EUR'][new_security.index.min()]):
            raise Exception("Not enough funds")

        self.tabulation = pd.concat([self.tabulation, new_security], axis = 1, join = 'outer')
        
        self.tabulation[ticker] = self.tabulation[ticker]*self.exchangeRates['EUR_'+currency]*amountShares

        self.tabulation['EUR'][new_security.index.min():] -= purchase_price
        if (endDate != date.today()):
            self.tabulation['EUR'][new_security.index.max():] += new_security[ticker][new_security.index.max()]*self.exchangeRates['EUR_'+currency][new_security.index.min()]*amountShares

        for index in [startDate + timedelta(days=x) for x in range(0, (endDate-startDate).days)]:
            if (np.isnan(self.tabulation[ticker][index])):
                self.tabulation[ticker][index] = self.tabulation[ticker][index-timedelta(days=1)] 






