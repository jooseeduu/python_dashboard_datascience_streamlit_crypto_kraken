import View

class Project_MBDS:

    name_project ="";

    def __init__(self,name_project):
        self.name_project  = name_project;

    def start_view(self):
        view_streamlit = View.Streamlit()
        view_streamlit.get_title(self.name_project)
        view_streamlit.show_status()
        view_streamlit.get_sidebar()
        view_streamlit.get_price_chart()
        view_streamlit.get_moving_average_chart()
        view_streamlit.get_rsi_chart()
        view_streamlit.get_moving_average_and_price_chart()
        view_streamlit.get_dataframe()
        print('Project run successfully')

#Inicializamos el proyecto.
project = Project_MBDS("Proyecto de Python Para el Análisis de Datos")
project.start_view()

