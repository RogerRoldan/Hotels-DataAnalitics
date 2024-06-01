import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from urllib.error import URLError
import plotly.express as px
import folium

# wide mode
st.set_page_config(
    page_title="Entendiendo los datos", 
    page_icon="🤔",
    layout="wide",
    initial_sidebar_state="expanded",
) 

data = pd.read_csv('data/hotel_bookings.csv')

# Función para configurar el estado de la página
def set_page(page):
    st.session_state.page = page
    st.experimental_rerun()

# Configurar el estado inicial de la página
if 'page' not in st.session_state:
    st.session_state.page = 'datos'

# Barra lateral para navegación
st.sidebar.title('Navegación')
if st.sidebar.button('Vista de datos'):
    set_page('datos')
if st.sidebar.button('Variables numéricas'):
    set_page('variables_numericas')
if st.sidebar.button('Variables categóricas'):
    set_page('variables_categoricas')
if st.sidebar.button('Datos atipicos'):
    set_page('atipicos')
if st.sidebar.button('Tasas'):
    set_page('tasas')
if st.sidebar.button('Tendencias'):
    set_page('tendencia')
if st.sidebar.button('Mapa coroplético'):
    set_page('mapa_coropletico')



# Página datos
if st.session_state.page == 'datos':

    st.markdown("# Entendiendo los datos")
    st.write(
        """En esta sección se describe el contenido del dataset de reservas de hotel, indicando los atributos del dataset y las fuentes de datos."""
    )
    st.title('Vista previa de los datos')
    st.write('Aquí tienes una vista previa de los datos:')
    st.write(data.head())

    st.write("### Dimensión de los datos")
    st.write("**El conjunto de datos contiene 119390 filas y 32 columnas.**")

    st.write("### Descripción de los atributos")
    st.write(
        """
        - `hotel`: Tipo de hotel (Resort Hotel o City Hotel).
        - `is_canceled`: Indicador de si la reserva fue cancelada (1) o no (0).
        - `lead_time`: Días entre la reserva y el check-in.
        - `arrival_date_year`: Año de llegada.
        - `arrival_date_month`: Mes de llegada.
        - `arrival_date_week_number`: Semana del año de llegada.
        - `arrival_date_day_of_month`: Día del mes de llegada.
        - `stays_in_weekend_nights`: Número de noches de fin de semana (sábado y domingo).
        - `stays_in_week_nights`: Número de noches entre semana (lunes a viernes).
        - `adults`: Número de adultos.
        - `children`: Número de niños.
        - `babies`: Número de bebés.
        - `meal`: Tipo de comida reservada.
        - `country`: País de origen del cliente.
        - `market_segment`: Segmento de mercado.
        - `distribution_channel`: Canal de distribución.
        - `is_repeated_guest`: Indicador de si el cliente es repetitivo (1) o no (0).
        - `previous_cancellations`: Número de cancelaciones previas.
        - `previous_bookings_not_canceled`: Número de reservas previas no canceladas.
        - `reserved_room_type`: Tipo de habitación reservada.
        - `assigned_room_type`: Tipo de habitación asignada.
        - `booking_changes`: Número de cambios en la reserva.
        - `deposit_type`: Tipo de depósito (No Deposit, Non Refund, Refundable).
        - `agent`: ID del agente que hizo la reserva.
        - `company`: ID de la compañía que hizo la reserva.
        - `days_in_waiting_list`: Número de días en lista de espera.
        - `customer_type`: Tipo de cliente (Contract, Group, Transient, Transient-party).
        - `adr`: Tarifa diaria promedio.
        - `required_car_parking_spaces`: Número de plazas de aparcamiento requeridas.
        - `total_of_special_requests`: Número total de solicitudes especiales.
        - `reservation_status`: Estado de la reserva (Canceled, Check-Out, No-Show).
        - `reservation_status_date`: Fecha del estado de la reserva.
        """
    )

    st.write("### Tipos de datos")
    st.write(data.dtypes)

    st.write("### Estadísticas descriptivas")
    st.write("Las estadísticas descriptivas del conjunto de datos nos permiten obtener información sobre la distribución de los datos, como la media, la mediana, la desviación estándar, etc.")
    st.write(data.describe())

    st.write("Ahora visualizamos a las variables categóricas, donde podremos observar solo las columnas que son categóricas (de tipo object):")
    st.write(data.describe(include=['object']))

    st.write("### Valores nulos o datos faltantes")
    st.write("Los valores nulos del conjusto de datos representan la cantidad de valores nulos por cada atributo:")
    st.write(data.isnull().sum())


    st.write("### Valores duplicados")
    st.write("Para ver los datos duplicados del conjunto de datos llamamos al método duplicated() en el DataFrame. Si luego llamamos al método SUM, obtendremos el total de duplicados:")
    st.write("Total duplicados: ",data.duplicated().sum())

    st.write("### Filas duplicadas")
    st.write(data[data.duplicated()])



# Página datos atípicos
if st.session_state.page == 'atipicos':
    st.title('Datos atípicos')
    st.write('En esta sección se describen algunos de los datos atípicos del dataset de reservas de hotel.')


    # Visualización de datos atípicos
    st.write("### Visualización de datos atípicos")

    # Visualización de la distribución de la tarifa diaria promedio
    st.write("Visualización grafica del diagrama de caja de la tarifa diaria promedio:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='adr', data=data, ax=ax)
    ax.set_title('Distribución de la tarifa diaria promedio')
    plt.xlabel("Tarifa diaria promedio")
    st.pyplot(fig)
    st.write("---")

    # También se pueden analizar los datos utilizando alguna variable categórica, por ejemplo, las reservas canceladas o no canceladas y vincularlo a una variable numérica como las noches de fin de semana:
    st.write("También se pueden analizar los datos utilizando alguna variable categórica, por ejemplo, las reservas canceladas o no canceladas y vincularlo a una variable numérica como las noches de fin de semana:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='is_canceled', y='stays_in_weekend_nights', data=data, ax=ax)
    ax.set_title('Distribución de las noches de fin de semana por tipo de reserva')
    plt.xlabel("0 - No cancelada, 1 - Cancelada")
    plt.ylabel("Noches de fin de semana")
    st.pyplot(fig)
    st.write("Donde 0 indica que la reserva no fue cancelada y 1 indica que la reserva fue cancelada.")
    st.write("---")


    # Visualización de la distribución de la duración de la estancia
    st.write("Podemos visualizar graficamente la distribución de la duración de la estancia:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='stays_in_weekend_nights', data=data, ax=ax)
    ax.set_title('Distribución de la duración de la estancia')
    plt.xlabel("Número de noches de fin de semana")
    st.pyplot(fig)
    st.write("---")



# Página tasas
if st.session_state.page == 'tasas':
    st.title('Tasas')
    st.write('En esta sección se describen algunas de las tasas del dataset de reservas de hotel.')


    # Visualización de las tasas
    st.write("### Visualización de tasas")

    # Visualización de la tasa de cancelación
    st.write("Visualización de la tasa de cancelación:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='is_canceled', y='is_canceled', data=data, estimator=lambda x: len(x) / len(data) * 100, ax=ax)
    ax.set(ylabel="Porcentaje")
    ax.set_title('Tasa de cancelación')
    plt.xlabel("Cancelada (1) / No cancelada (0)")
    st.pyplot(fig)
    st.write("Donde 0 indica que la reserva no fue cancelada y 1 indica que la reserva fue cancelada.")
    st.write("---")

    # Visualización de la tasa de cancelación por tipo de hotel
    st.write("Visualización de porcentaje de cancelación por tipo de hotel:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='hotel', y='is_canceled', data=data, estimator=lambda x: len(x) / len(data) * 100, ax=ax)
    ax.set(ylabel="Porcentaje")
    ax.set_title('Tasa de cancelación por tipo de hotel')
    st.pyplot(fig)
    st.write(
        """
        - City Hotel: Hotel urbano.
        - Resort Hotel: Hotel resort.
        """
    )
    st.write("---")


    # Combinando variables
    # sns.countplot(data=df, x = 'hotel', hue='is_canceled')
    # plt.show()
    st.write(
        """
            Después de analizar las variables de manera individual para comprender su comportamiento, se pueden encontrar relaciones interesantes entres dos, tres o cuatro variables. A continuación se responden algunas preguntas interesantes:

        - ¿Qué tipo de hotel tiene el mayor número de cancelaciones?
    """)
    st.write("Visualización de la tasa de cancelación por tipo de hotel:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=data, x='hotel', hue='is_canceled', ax=ax)
    ax.set_title('Tasa de cancelación por tipo de hotel')
    plt.xlabel("Tipo de hotel")
    plt.ylabel("Reservas")
    st.pyplot(fig)
    st.write("---")



    # Visualización de la tasa de cancelación por tipo de cliente
    st.write("Visualización de porcentaje de cancelación por tipo de cliente:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='customer_type', y='is_canceled', data=data, estimator=lambda x: len(x) / len(data) * 100, ax=ax)
    ax.set(ylabel="Porcentaje", xlabel="Tipo de cliente")
    ax.set_title('Tasa de cancelación por tipo de cliente')
    st.pyplot(fig)
    st.write(
        """ 
        - Contract: Contrato (reservas de grupo o contrato).
        - Group: Grupo (reservas de grupo).
        - Transient: Transitorio (reservas individuales no asociadas a un grupo).
        - Transient-party: Grupo transitorio (reservas individuales asociadas a un grupo).
        """
    )
    st.write("---")


    # Visualización de la tasa de cancelación por tipo de comida
    st.write("Visualización de la porcentaje de cancelación por tipo de comida:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='meal', y='is_canceled', data=data, ax=ax)
    ax.set_title('Tasa de cancelación por tipo de comida')
    ax.set(ylabel="Porcentaje")
    st.pyplot(fig)
    st.write(
        """
        - BB: Bed & Breakfast.
        - HB: Half Board (desayuno y cena).
        - FB: Full Board (desayuno, almuerzo y cena).
        - SC: Sin comida.
        """
    )
    st.write("---")

    # Análisis de las reservas que no fueron canceladas, según el segmento del mercado:
    # Separamos los grupos por tipo de hotel y solo con reservas no canceladas:
    rh = data[(data['hotel'] == 'Resort Hotel') & (data['is_canceled'] == 0)]
    ch = data[(data['hotel'] == 'City Hotel') & (data['is_canceled'] == 0)]
    # Visualización de los gráficos de torta
    st.write("### Distribución del segmento de mercado")

    # Gráfico de torta para Resort Hotel
    st.write("#### El segmento de mercado del hotel resort")
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    rh_segment_pie = rh['market_segment'].value_counts()
    ax1.pie(rh_segment_pie, labels=rh_segment_pie.index, autopct='%.3f%%')
    ax1.set_title('El segmento de mercado del hotel resort')
    st.pyplot(fig1)

    # Gráfico de torta para City Hotel
    st.write("#### El segmento de mercado del Hotel City")
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ch_segment_pie = ch['market_segment'].value_counts()
    ax2.pie(ch_segment_pie, labels=ch_segment_pie.index, autopct='%.3f%%')
    ax2.set_title('El segmento de mercado del Hotel City')
    st.pyplot(fig2)




# Analisis de tendencia central, posicion y dispersion
if st.session_state.page == 'tendencia':
    st.title('Análisis de tendencia central, posición y dispersión')
    st.write('En esta sección se realiza un análisis de tendencia central, posición y dispersión del dataset de reservas de hotel.')


    st.write("### Análisis de tendencia central, posición y dispersión")
    st.write("""
             El análisis de la tendencia central, la simetría y la dispersión de los datos es importante para entender cómo se comporta cada variable y una variable que nos puede ayudar a entender esto es la variable `lead_time`.

            - lead_time: número de días entre hecha la reserva y el día de llegada al hotel.
    """)
    st.write("#### lead_time")
    st.write("Media: ", data['lead_time'].mean())
    st.write("Mediana: ", data['lead_time'].median())
    st.write("Desviación estándar: ", data['lead_time'].std())
    st.write("Mínimo: ", data['lead_time'].min())
    st.write("Máximo: ", data['lead_time'].max())

    st.write("### Análisis de la distribución de los datos")
    st.write("La distribución de los datos nos permite entender cómo se distribuyen los valores de una variable en un conjunto de datos. Para ello, podemos utilizar histogramas, diagramas de caja, entre otros.")
    st.write("#### lead_time")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['lead_time'], kde=True, ax=ax)
    ax.set_title('Distribución de lead_time')
    plt.xlabel("Días entre la reserva y la llegada al hotel")
    plt.ylabel("Reservas")
    st.pyplot(fig)
    st.write("Este grafico nos muestra que la mayoría de las reservas se realizan con un lead_time de 0 a 100 días, con un pico en 0 días, lo que indica que la mayoría de las reservas se realizan el mismo día de la llegada al hotel.")
    st.write("---")

    # Visualización de la distribución de la tarifa diaria promedio
    st.write("Visualización de la distribución de la tarifa diaria promedio:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['adr'], kde=True, ax=ax)
    ax.set_title('Distribución de la tarifa diaria promedio')
    plt.xlabel("Tarifa diaria promedio")
    plt.ylabel("Reservas")
    ax.set_xlim(0, 1000) 
    st.pyplot(fig)
    st.write("En el eje x se muestra la tarifa diaria promedio y en el eje y el número de reservas.")
    st.write("---")

    # Visualización de la distribución de la duración de la estancia
    st.write("Visualización de la distribución de la duración de la estancia:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['stays_in_weekend_nights'], kde=True, ax=ax)
    ax.set_title('Distribución de la duración de la estancia')
    plt.xlabel("Número de noches de fin de semana")
    plt.ylabel("Reservas")
    st.pyplot(fig)
    st.write("---")


   # Visualización del número de la semana del año en que llega el huesped al hotel.
    st.write("Visualización de la distribución del número de la semana del año en que llega el huésped al hotel:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['arrival_date_week_number'], kde=True, ax=ax)
    ax.set_title('Distribución del número de la semana del año en que llega el huésped al hotel')
    plt.xlabel("Número de la semana del año")
    plt.ylabel("Reservas")
    st.pyplot(fig)

    # Sus estadísticas descriptivas son:
    st.write("#### arrival_date_week_number")
    st.write("Media: ", data['arrival_date_week_number'].mean())
    st.write("Mediana: ", data['arrival_date_week_number'].median())
    st.write("Desviación estándar: ", data['arrival_date_week_number'].std())
    st.write("Mínimo: ", data['arrival_date_week_number'].min())
    st.write("Máximo: ", data['arrival_date_week_number'].max())
    st.write("---")



    # Inclinación de los clientes por los distintos tipos de habitación:
    st.write("Visualización de la inclinación de los clientes por los distintos tipos de habitación:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='reserved_room_type', data=data, ax=ax)
    ax.set_title('Inclinación de los clientes por los distintos tipos de habitación')
    plt.xlabel("Tipo de habitación reservada")
    plt.ylabel("Reservas")
    st.pyplot(fig)
    st.write("En el eje x se muestra el tipo de habitación reservada y en el eje y el número de reservas.")
    st.write("---")


    # Visualización de por donde se realiza la reserva:
    st.write("Visualización de por donde se realiza la reserva:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='market_segment', data=data, ax=ax)
    ax.set_title('Distribución de las reservas por canal de distribución')
    plt.xlabel("Canal de distribución")
    plt.ylabel("Reservas")
    st.pyplot(fig)
    st.write("En el eje x se muestra el canal de reservación y en el eje y el número de reservas.")
    st.write("---")



# Página variables numéricas df.hist(figsize=(20,15))
if st.session_state.page == 'variables_numericas':
    st.title('Variables numéricas')
    st.write('En esta sección se describen algunas de las variables numéricas del dataset de reservas de hotel.')


    st.write("### Visualización de variables numéricas")

    # Visualización de las variables numéricas
    st.write("Visualización de las variables numéricas del conjunto de datos:")
    st.write(data.describe())

    st.write("### Distribución de las variables numéricas")
    st.write("La distribución de las variables numéricas nos permite entender cómo se distribuyen los valores de cada variable en un conjunto de datos. Para ello, podemos utilizar histogramas, diagramas de caja, entre otros.")
    st.write("#### Histograma de las variables numéricas")
    st.write("En el siguiente histograma se muestra la distribución de las variables numéricas del conjunto de datos.")
    fig, ax = plt.subplots(figsize=(20, 15))
    data.hist(ax=ax)
    plt.tight_layout()
    st.pyplot(fig)
    st.write("En el eje x se muestra el rango de valores de cada variable y en el eje y el número de reservas.")
    st.write("---")



# Página variables categóricas
if st.session_state.page == 'variables_categoricas':
    st.title('Variables categóricas')
    st.write('En esta sección se describen algunas de las variables categóricas del dataset de reservas de hotel.')


    st.write("### Visualización de variables categóricas")

    # Visualización de las variables categóricas
    st.write("Visualización de las variables categóricas del conjunto de datos:")
    st.write(data.describe(include=['object']))

    st.write("### Distribución de las variables categóricas")
    st.write("La distribución de las variables categóricas nos permite entender cómo se distribuyen los valores de cada variable en un conjunto de datos. Para ello, podemos utilizar gráficos de barras, entre otros.")
    st.write("#### Tipo de hotel")
    st.write("Visualización de la distribución del tipo de hotel:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='hotel', data=data, ax=ax)
    ax.set_title('Distribución del tipo de hotel')
    plt.xlabel("Tipo de hotel")
    plt.ylabel("Reservas")
    st.pyplot(fig)
    st.write(
        """
        - City Hotel: Hotel urbano.
        - Resort Hotel: Hotel resort.
        """
    )
    st.write("---")

    st.write("""
        Para analizar las variables categóricas, seleccionamos primero el subconjunto del dataframe y visualizamos los valores de cada categoría. Identificamos algún valor que no corresponda con el negocio.
    """)
    
    st.write("### Visualización de las variables categóricas")
    st.write("Visualización de las variables categóricas del conjunto de datos:")
    st.write(data.select_dtypes(include=['object']).head())
    st.write("- La columna reservation_status_date se muestra como tipo de dato categórico, sin embargo, debería de ser datetime64 más adelante se hará el cambio.")

    st.write("### Visualizar los valores de cada una de las variables:")
    st.write("- Esto nos ayuda a identificar valores que no coinciden con el dominio del negocio, de ser así, lo eliminaríamos.")


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write("#### Tipo de hotel")
        st.table(data['hotel'].unique())

        st.write("#### Mes de llegada")
        st.table(data['arrival_date_month'].unique())

        st.write("#### Tipo de depósito")
        st.table(data['deposit_type'].unique())
        
        st.write("#### ID del agente")
        st.write(data['agent'].unique())

    with col2:
        st.write("#### Estado de la reserva")
        st.table(data['reservation_status'].unique())

        st.write("#### Segmento de mercado")
        st.table(data['market_segment'].unique())

        st.write("#### Canal de distribución")
        st.table(data['distribution_channel'].unique())

    with col3:
        st.write("#### Tipo de comida")
        st.table(data['meal'].unique())
        

        st.write("#### Tipo de cliente")
        st.table(data['customer_type'].unique())

        st.write("#### País de origen del cliente")
        st.write(data['country'].unique())


    with col4:
        st.write("#### Tipo de habitación reservada")
        st.table(data['reserved_room_type'].unique())

        st.write("#### Tipo de habitación asignada")
        st.table(data['assigned_room_type'].unique())

    with col5:
        st.write("#### ID de la compañía")
        st.write(data['company'].unique())
        
        st.write("#### Fecha del estado de la reserva")
        st.write(data['reservation_status_date'].unique())


# Página mapa coroplético
if st.session_state.page == 'mapa_coropletico':
    st.title('Mapa coroplético')
    st.write('En esta sección se muestra un mapa coroplético con la distribución de las reservas de hotel por país.')

    # Crear el mapa de folium
    basemap = folium.Map()

    # Obtener los datos de los países más visitados
    paises_mas_visitas = data[data['is_canceled'] == 0]['country'].value_counts().reset_index()
    paises_mas_visitas.columns = ['country', 'No of guests']

    # Crear el gráfico de choropleth con Plotly
    guests_map = px.choropleth(
        paises_mas_visitas,
        locations='country',
        color='No of guests',
        color_continuous_scale="portland",
        hover_name='country'
    )

    # Mostrar el gráfico de choropleth en Streamlit
    st.plotly_chart(guests_map)

    st.write(
        """
             Los países con colores mas fríos son los que tienen menos reservas de hotel, mientras que los países con colores más cálidos son los que tienen más reservas de hotel.
        """
    )

    st.write("#### Estos son los 10 países con más reservas de hotel:")
    st.write(paises_mas_visitas.head(10))

