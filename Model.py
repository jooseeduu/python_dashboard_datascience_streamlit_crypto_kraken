from APIKraken import *
import pandas as pd
class ModelAssets:

    __selected_tradable_asset_pair = None

    __dataframe_selected_tradable_asset_pair = None

    __period_moving_average = None

    __period_rsi = None

    def __init__(self):

        None

    def get_status_kraken(self):

        api = APIKraken()

        status = api.get_status()

        return status


    def get_list_tradable_asset_pairs(self):

        api = APIKraken()

        api_tradable_asset_pairs = api.get_list_tradable_asset_pairs()

        api_result_tradable_asset_pairs = list(api_tradable_asset_pairs['result'].values())

        list_tradable_asset_pairs = []

        for tradable_asset_pairs in api_result_tradable_asset_pairs:

            list_tradable_asset_pairs.append(tradable_asset_pairs['wsname'])

        return list_tradable_asset_pairs


    def get_dataframe_selected_tradable_asset_pair(self):

        return self.__dataframe_selected_tradable_asset_pair

    def get_period_moving_average(self):

        return self.__period_moving_average

    def get_period_rsi(self):

        return self.__period_rsi

    def set_dataframe_selected_tradable_asset_pair(self, minutes ):

        api = APIKraken()

        api_dataframe_selected_tradable_asset_pair = api.get_OHLC( self.__selected_tradable_asset_pair.replace("/", "" ) ,minutes )

        api_result_dataframe_selected_tradable_asset_pair = list(api_dataframe_selected_tradable_asset_pair['result'].values())[0]

        #convertimos el resultado en un dataframe
        dataframe_result = pd.DataFrame(api_result_dataframe_selected_tradable_asset_pair, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])

        #el campo time se encuentra en intunixtime , lo convertimos a un campo tipo datetime
        dataframe_result['time'] = pd.to_datetime(dataframe_result['time'], unit='s')

        #por úlitmo las siguientes columnas las especificamos cómo numéricas
        cols = ['open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
        dataframe_result[cols] = dataframe_result[cols].apply(pd.to_numeric, errors='coerce', axis=1)

        self.__add_to_dataframe_moving_average(dataframe_result, self.__period_moving_average)

        self.__add_to_dataframe_rsi(dataframe_result , self.__period_rsi )

        self.__dataframe_selected_tradable_asset_pair = dataframe_result

        return None



    def get_selected_tradable_asset_pair(self):

        return self.__selected_tradable_asset_pair


    def set_selected_tradable_asset_pair(self,selected_tradable_asset_pair):

        self.__selected_tradable_asset_pair = selected_tradable_asset_pair

        return None

    def set_period_moving_average(self,period_moving_average):

        self.__period_moving_average = period_moving_average

        return None

    def set_period_rsi(self,period_rsi):

        self.__period_rsi = period_rsi

        return None



    def __add_to_dataframe_moving_average(self , dataframe, interval_value = 3 , int_shift = 1 ):

        dataframe['moving_average'] = dataframe['close'].rolling(interval_value).mean().shift(int_shift)

        return dataframe

    def __add_to_dataframe_rsi(self, dataframe , rsi_period =  14 ):

        chg = dataframe.close.diff(1)
        gain = chg.mask(chg < 0, 0)
        dataframe['gain'] = gain

        loss = chg.mask(chg > 0, 0)
        dataframe['loss'] = loss

        avg_gain = gain.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        avg_loss = loss.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()

        dataframe['avg_gain'] = avg_gain
        dataframe['avg_loss'] = avg_loss

        rs = abs(avg_gain / avg_loss)

        rsi = 100 - (100 / (1 + rs))

        dataframe['rsi'] = rsi

        return dataframe


