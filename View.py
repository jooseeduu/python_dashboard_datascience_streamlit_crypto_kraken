import streamlit as st
from Controller import *
from datetime import datetime

class Streamlit:

    controller_assets = None

    def __init__(self):

        self.controller_assets = ControllerAssets()

        st.set_page_config(
            page_title="Master Big Data Science",
            page_icon="🧊",
            layout="wide",
            initial_sidebar_state="expanded"
        )


    def get_title(self,title):

        st.markdown("<h1 style='text-align: center; color: grey;'>"+title+"</h1>", unsafe_allow_html=True)


    def get_sidebar(self):

        list_tradable_asset_pairs = self.controller_assets.get_list_tradable_asset_pairs()

        default_value = list_tradable_asset_pairs.index('ETH/USDT')

        selected_tradable_asset_pair = st.sidebar.selectbox('Seleccione el Par de Activos',list_tradable_asset_pairs, index = default_value )

        list_period_time =  ('1 Minuto','5 Minutos','15 Minutos', '30 Minutos', '1 Hora', '4 Horas' ,'1 Día' , '1 Semana' , '15 Días');

        default_value = list_period_time.index('1 Día')

        selected_period_time = st.sidebar.selectbox('Seleccione el intervalo de tiempo',list_period_time, index = default_value)

        self.controller_assets.set_selected_tradable_asset_pair(selected_tradable_asset_pair)

        self.controller_assets.set_dataframe_selected_tradable_asset_pair(selected_period_time)

        st.sidebar.write("Actualizado al:" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



    def get_price_chart(self):

        dataframe = self.controller_assets.get_dataframe_price_chart()

        st.area_chart(dataframe)


    def get_moving_average_chart(self):

        dataframe = self.controller_assets.get_dataframe_moving_average_chart()

        st.line_chart(dataframe)


    def get_rsi_chart(self):

        dataframe = self.controller_assets.get_dataframe_rsi_chart()

        st.line_chart(dataframe)


    def get_moving_average_and_price_chart(self):

        dataframe = self.controller_assets.get_dataframe_moving_average_and_price_chart()

        st.line_chart(dataframe)


    def get_dataframe(self):

        dataframe = self.controller_assets.get_dataframe_selected_tradable_asset_pair()

        st.dataframe(dataframe, use_container_width=True)

        df_xlsx = self.controller_assets.to_excel(dataframe)


        st.download_button(label='📥 Download Current Result ',
                           data=df_xlsx,
                           file_name='dataframe.xlsx')
