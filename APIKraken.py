from requests.exceptions import HTTPError
import krakenex
import pandas as pd

class APIKraken:

    kraken = None

    def __init__(self):
        self.kraken = krakenex.API()
        None


    def get_assets(self):
        try:
            response = self.kraken.query_public('Assets')
            list_assets = list(response['result'].keys())
        except HTTPError as e:
            print(str(e))
        return list_assets


    def get_list_tradable_asset_pairs(self):
        kraken = krakenex.API()
        try:
            response = kraken.query_public('AssetPairs')
        except HTTPError as e:
            print(str(e))
        return response


    def get_OHLC(self,selected_tradable_asset_pair , interval  ):
        kraken = krakenex.API()
        try:
            # response = kraken.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '10'})
            response = kraken.query_public('OHLC', {'pair': selected_tradable_asset_pair  , 'interval': interval  })
            #print(response)
            # pprint.pprint(response)
        except HTTPError as e:
            print(str(e))

        return response


#api = KrakenData()
#data = api.get_asset_tradable()
#print(data)
#import requests
#resp = requests.get('https://api.kraken.com/0/public/Time')
#print('TIME',resp.json())

##CHECK STATUS KRAKEN
#resp = requests.get('https://api.kraken.com/0/public/SystemStatus')
#print(resp.json())

##LIST ASSETS
#resp = requests.get('https://api.kraken.com/0/public/Assets')
#print(resp.json())

##https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData
#resp = requests.get('https://api.kraken.com/0/public/OHLC?pair=XBTUSD')
#print(resp.json())


