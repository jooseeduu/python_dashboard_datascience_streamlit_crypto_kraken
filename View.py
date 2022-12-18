import streamlit as st
import altair as alt
from Controller import *
from datetime import datetime

#https://altair-viz.github.io/gallery/index.html


#https://altair-viz.github.io/user_guide/marks.html

class Streamlit:

    __controller_assets = None

    def __init__(self):

        self.__controller_assets = ControllerAssets()

        st.set_page_config(
            page_title="Master Big Data Science",
            page_icon="🧊",
            layout="wide",
            initial_sidebar_state="expanded"
        )


    def get_title(self,title):

        st.markdown("<h1 style='text-align: center; color: grey;'>"+title+"</h1>", unsafe_allow_html=True)

    def show_status(self):

        status = self.__controller_assets.get_status_kraken()

        if(status != 'online'):
            st.error('El servicio de Kraken no está disponible', icon="⛔")
            print('El servicio de Kraken no está disponible')
            exit(1)







    def get_sidebar(self):

        list_tradable_asset_pairs = self.__controller_assets.get_list_tradable_asset_pairs()

        default_value = list_tradable_asset_pairs.index('ETH/USDT')

        selected_tradable_asset_pair = st.sidebar.selectbox('Seleccione el Par de Activos',list_tradable_asset_pairs, index = default_value )

        list_period_time =  ('1 Minuto','5 Minutos','15 Minutos', '30 Minutos', '1 Hora', '4 Horas' ,'1 Día' , '1 Semana' , '15 Días');

        default_value = list_period_time.index('1 Día')

        selected_period_time = st.sidebar.selectbox('Seleccione el Intervalo de Tiempo',list_period_time, index = default_value)

        period_moving_average = st.sidebar.slider('Período para la Media Móvil', 1, 30, 3)

        self.__controller_assets.set_period_moving_average(period_moving_average)

        self.__controller_assets.set_selected_tradable_asset_pair(selected_tradable_asset_pair)

        self.__controller_assets.set_dataframe_selected_tradable_asset_pair(selected_period_time)

        st.sidebar.write("Fuente de Datos: [kraken](https://www.kraken.com/)")

        st.sidebar.write("Data actualizada al:" + datetime.now().strftime('%d %B, %Y %H:%M:%S')  + "(UTC)")




    def get_price_chart(self):

        dataframe = self.__controller_assets.get_dataframe_price_chart()
        #st.area_chart(dataframe)
        selected_tradable_asset_pair = self.__controller_assets.get_selected_tradable_asset_pair()

        chart = alt.Chart(dataframe).mark_area(
            line={'color': 'darkgreen'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                       alt.GradientStop(color='darkgreen', offset=1)],
                x1=1,
                x2=1,
                y1=1,
                y2=0
            )
        ).encode(
            alt.X('time:T'),
            alt.Y('close:Q')
        ).properties(
            title="COTIZACIÓN - "+ selected_tradable_asset_pair,
        )

        st.altair_chart(chart, theme="streamlit", use_container_width=True)


        #tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

        #with tab1:
        #    st.altair_chart(chart, theme="streamlit", use_container_width=True)

        #with tab2:
        #    st.altair_chart(chart, theme="streamlit", use_container_width=True)



    def get_moving_average_chart(self):

        dataframe = self.__controller_assets.get_dataframe_moving_average_chart()

        selected_tradable_asset_pair = self.__controller_assets.get_selected_tradable_asset_pair()

        #st.write("I'm ", period_moving_average, 'years old')
        #st.line_chart(dataframe)
        #source = data.stocks()
        #print("------------------------------------------------DATAFRAME:")
        #print(dataframe.info())


        chart = alt.Chart(dataframe).mark_area(
            line={'color': 'darkblue'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                       alt.GradientStop(color='darkblue', offset=1)],
                x1=1,
                x2=1,
                y1=1,
                y2=0
            )
        ).encode(
            alt.X('time:T'),
            alt.Y('moving_average:Q')
        ).properties(
            title="MEDIA MÓVIL - "+ selected_tradable_asset_pair ,
        )

        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    def get_rsi_chart(self):

        dataframe = self.__controller_assets.get_dataframe_rsi_chart()
        selected_tradable_asset_pair = self.__controller_assets.get_selected_tradable_asset_pair()


        chart = alt.Chart(dataframe).mark_area(
            line={'color': 'darkred'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                       alt.GradientStop(color='darkred', offset=1)],
                x1=1,
                x2=1,
                y1=1,
                y2=0
            )
        ).encode(
            alt.X('time:T'),
            alt.Y('rsi:Q')
        ).properties(
            title="RSI - "+ selected_tradable_asset_pair,
        ).interactive()

        line_70 = alt.Chart(pd.DataFrame({'rsi': [70]})).mark_rule(strokeDash=[10, 10], size=2).encode(y='rsi')
        line_30 = alt.Chart(pd.DataFrame({'rsi': [30]})).mark_rule(strokeDash=[10, 10], size=2).encode(y='rsi')



        st.altair_chart(chart + line_70 + line_30, theme="streamlit", use_container_width=True)


        #st.line_chart(dataframe)


    def get_moving_average_and_price_chart(self):

        dataframe = self.__controller_assets.get_dataframe_moving_average_and_price_chart()
        selected_tradable_asset_pair = self.__controller_assets.get_selected_tradable_asset_pair()


        #st.help(dataframe)

        instructions = """
        Arrastre el cursor para ver los valores en el período seleccionado\n
        Podríamos agregar otros valores para compararlos en el período de tiempo
        """
        select_packages = st.multiselect(
            "Seleccione la Comparación de Métricas (" +selected_tradable_asset_pair+")" ,
            dataframe.columns.tolist(),
            default=[
                "close",
                "moving_average",

            ],
            help=instructions,
        )

        # Styler
        st.markdown("""
            <style>
                span[data-baseweb="tag"][aria-label="close, close by backspace"]{
                    background-color: green;
                }
                span[data-baseweb="tag"][aria-label="moving_average, close by backspace"]{
                    background-color: blue;
                }
                span[data-baseweb="tag"][aria-label="option3, close by backspace"]{
                    background-color: black;
                }
            </style>
            """, unsafe_allow_html=True)

        base = alt.Chart(dataframe.reset_index()).encode(x='time')

        if(len(select_packages) == 2 ):
            chart_1 = alt.layer(
                base.mark_line(color='green').encode(y='close'),
                base.mark_line(color='blue').encode(y='moving_average')
            ).interactive()
        elif(len(select_packages) == 0 ):
            chart_1 = alt.layer(
            ).interactive()
        elif (len(select_packages) == 1 and select_packages[0]== "close" ):
            chart_1 = alt.layer(
                base.mark_line(color='green').encode(y='close')
            ).interactive()
        elif (len(select_packages) == 1 and select_packages[0]== "moving_average" ):
            chart_1 = alt.layer(
                base.mark_line(color='blue').encode(y='moving_average')
            ).interactive()

        dataframe = dataframe.reset_index().melt('time', var_name='category', value_name='y')

        source = dataframe


        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['time'], empty='none')

        # The basic line

        #scale = alt.Scale(domain=['moving_average', ' close'], range=['gold', 'red'])
        #color = alt.Color('variable:N', scale=scale)


        line = alt.Chart(source).mark_line(interpolate='basis').encode(
            x='time:T',
            y='y:Q'
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='time:T',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'y:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='time:T',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        chart = alt.layer(
            chart_1, selectors, points, rules, text
        ).properties(
            width=600, height=300
        )

        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        #st.altair_chart(select_packages, theme="streamlit", use_container_width=True)




    def get_dataframe(self):

        dataframe = self.__controller_assets.get_dataframe_selected_tradable_asset_pair()
        selected_tradable_asset_pair = self.__controller_assets.get_selected_tradable_asset_pair()

        df_xlsx = self.__controller_assets.to_excel(dataframe)
        st.download_button(label='📥 DATAFRAME ('+ selected_tradable_asset_pair+')',
                           data=df_xlsx,
                           file_name='Dataframe ('+ selected_tradable_asset_pair+').xlsx' )

        st.dataframe(dataframe, use_container_width=True)





