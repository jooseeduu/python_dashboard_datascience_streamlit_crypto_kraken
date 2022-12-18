from requests.exceptions import HTTPError
import krakenex

class APIKraken:

    __kraken = None

    def __init__(self):
        self.__kraken = krakenex.API()
        None


    def get_status(self):
        try:
            response = self.__kraken.query_public('SystemStatus')

            if(response['result']['status'] != 'online'):
                return 'El servicio de Kraken no está disponible'

        except HTTPError as e:
            return 'El servicio de Kraken no está disponible'

        return response['result']['status']

    def get_assets(self):
        try:
            response = self.__kraken.query_public('Assets')
            list_assets = list(response['result'].keys())
        except HTTPError as e:
            return str(e)
        return list_assets


    def get_list_tradable_asset_pairs(self):
        kraken = krakenex.API()
        try:
            response = self.__kraken.query_public('AssetPairs')
        except HTTPError as e:
            return str(e)
        return response


    def get_OHLC(self,selected_tradable_asset_pair , interval  ):

        kraken = krakenex.API()

        try:

            response = self.__kraken.query_public('OHLC', {'pair': selected_tradable_asset_pair  , 'interval': interval  })

        except HTTPError as e:

            return str(e)

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


