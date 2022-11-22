from io import BytesIO
from Model import ModelAssets
import pandas as pd
import xlsxwriter as xlsxwriter
import click

class ControllerAssets:

    model_assets = ModelAssets()

    def __init__(self):
        None


    def get_list_tradable_asset_pairs(self):

        return self.model_assets.get_list_tradable_asset_pairs()


    def set_selected_tradable_asset_pair(self, selected_tradable_asset_pair):

        self.model_assets.set_selected_tradable_asset_pair(selected_tradable_asset_pair)


    def set_dataframe_selected_tradable_asset_pair(self , selected_period_time ):

        minutes = 1 ;

        '1 Minuto', '5 Minutos', '15 Minutos', '30 Minutos', '1 Hora', '4 Horas', '1 Día', '1 Semana', '2 Semanas'


        if(selected_period_time == '1 Minuto' ):
            minutes  = 1
        elif (selected_period_time == '5 Minutos'):
            minutes = 5
        elif (selected_period_time == '15 Minutos'):
            minutes = 15
        elif (selected_period_time == '30 Minutos'):
            minutes = 30
        elif (selected_period_time == '1 Hora'):
            minutes = 60
        elif (selected_period_time == '4 Horas'):
            minutes = 240
        elif (selected_period_time == '1 Día'):
            minutes = 1440
        elif (selected_period_time == '1 Semana'):
            minutes = 10080
        elif (selected_period_time == '15 Días'):
            minutes = 21600
        else:
            minutes =1


        self.model_assets.set_dataframe_selected_tradable_asset_pair(minutes)

    def get_dataframe_selected_tradable_asset_pair(self):

        dataframe = self.model_assets.get_dataframe_selected_tradable_asset_pair()

        return dataframe

    def get_dataframe_price_chart(self):

        dataframe = self.get_dataframe_selected_tradable_asset_pair()

        chart_data = pd.DataFrame(dataframe, columns=['time', 'close'])

        chart_data = chart_data.set_index('time')

        return chart_data

    def get_dataframe_moving_average_chart(self):

        dataframe = self.get_dataframe_selected_tradable_asset_pair()

        chart_data = pd.DataFrame(dataframe, columns=['time', 'moving_average'])

        chart_data = chart_data.set_index('time')

        return chart_data

    def get_dataframe_rsi_chart(self):

        dataframe = self.get_dataframe_selected_tradable_asset_pair()

        chart_data = pd.DataFrame(dataframe, columns=['time', 'rsi'])

        chart_data = chart_data.set_index('time')

        return chart_data

    def get_dataframe_moving_average_and_price_chart(self):

        dataframe = self.get_dataframe_selected_tradable_asset_pair()

        chart_data = pd.DataFrame(dataframe, columns=['time', 'moving_average', 'close'])

        chart_data = chart_data.set_index('time')

        return chart_data


    def to_excel(self, df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.save()
        processed_data = output.getvalue()
        return processed_data


