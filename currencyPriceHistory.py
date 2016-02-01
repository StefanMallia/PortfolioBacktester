from urllib import request
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import json
import numpy as np


def currencyPriceHistory(startDate, endDate, tradeInfo):
    #returns currency pair midClose price ((ask+bid)/2) as a DataFrame
    if (not isinstance(startDate, date) or not isinstance(endDate, date) ):
        raise Exception("Dates should be inputted as date object from datetime")


    endpoint = 'https://api-' + tradeInfo.domain + '/v1/candles'\
               + '?instrument=' + tradeInfo.instrument_string\
               + '&granularity=' + tradeInfo.granularity\
               + '&start=' + startDate.strftime("%Y-%m-%d")\
               + '&end=' + endDate.strftime("%Y-%m-%d")\
               + '&include_First=False'             

    query_params = { 'Authorization': 'Bearer ' + tradeInfo.access_token }

    req = request.Request(endpoint, headers = query_params)
    response = request.urlopen(req)        
    data = response.read().decode('utf-8')        
    data = json.loads(data)
    data = pd.DataFrame([(data['candles'][x]['closeBid'] + data['candles'][x]['closeAsk'])/2 for x in range(len(data['candles']))],\
                        index = [datetime.strptime(data['candles'][x]['time'], '%Y-%m-%dT%H:%M:%S.%fZ').date() for x in range(len(data['candles']))],\
                        columns = [tradeInfo.instrument_string])
    return data


class TradeInfo:

    def __init__(self, domain, access_token, account_id, instrument_string, granularity):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.instrument_string = instrument_string
        self.granularity = granularity

