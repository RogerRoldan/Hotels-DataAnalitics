import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from urllib.error import URLError
import plotly.express as px
import folium
import numpy as np
from sklearn.neighbors import LocalOutlierFactor


st.set_page_config(page_title="Preparando los datos", page_icon="🛠️")

# Función para configurar el estado de la página
def set_page(page):
    st.session_state.page = page
    st.experimental_rerun()

# Configurar el estado inicial de la página
if 'page' not in st.session_state:
    st.session_state.page = 'limpieza'

# Barra lateral para navegación
st.sidebar.title('Navegación')
if st.sidebar.button('Limpieza de datos'):
    set_page('limpieza')
if st.sidebar.button('Tipos de datos'):
    set_page('tipos')
if st.sidebar.button('Datos inconsistentes'):
    set_page('inconsistentes')
if st.sidebar.button('Datos atípicos'):
    set_page('atipicos')
if st.sidebar.button('Datos redundantes'):
    set_page('redundantes')
if st.sidebar.button('Datos duplicados'):
    set_page('duplicados')





data = pd.read_csv('data/hotel_bookings.csv')



# PROCESO DE TRATAMIENTO DE LOS DATOS

# lIMPIEZA DE DATOS
# Eliminar los valores nulos de las columnas company, agent y children
cleanData = data.drop(columns=["company", "agent"], axis=1)
# Eliminar las filas con valores nulos en la columna children
cleanData1 = cleanData.dropna(subset=['country', 'children'], axis = 0)
# Sustituir los valores nulos de la columna children por 0 que es la mediana de la columna
cleanData1["children"].replace(np.nan, 0, inplace=True)


# TIPOS DE DATOS
# Cambiar el tipo de dato de la columna children a int
cleanData1["children"] = cleanData1["children"].astype(int)
# Cambiar el tipo de dato de la columna reservation_status_date a DateTime
cleanData1["reservation_status_date"] = pd.to_datetime(cleanData1["reservation_status_date"])


# DATOS INCONSISTENTES
# Eliminar las filas con (data.children == 0) & (data.adults == 0) & (data.babies == 0)
# inconsistentData = cleanData1[(cleanData1["children"] == 0) & (cleanData1["adults"] == 0) & (cleanData1["babies"] == 0)]
inconsistentData = (cleanData1.children == 0) & (cleanData1.adults == 0) & (cleanData1.babies == 0)

consistentData = cleanData1[~inconsistentData]



if st.session_state.page == 'limpieza':
    st.title('Limpieza de datos')

    st.write(
        """
        En esta sección se describe el proceso de limpieza de datos, indicando el contexto del problema, y los datos utilizados.
        """
    )

    st.write("### Valores nulos o datos faltantes")
    st.write("Los valores nulos del conjusto de datos representan la cantidad de valores nulos por cada atributo:")
    st.write(data.isnull().sum())

    st.write("### Eliminación de valores nulos")
    st.write("Eliminaremos los valores nulos del conjunto de datos:")
    st.write(data[["children", "country", "agent", "company"]].describe(include="all"))

    st.write(
        """
        - La cantidad de datos faltantes en la columna company hace que no sea útil sustituirlos o imputarlos, pues faltan muchos datos y modificarlos supondría una grave alteración de los datos.

        - La columna agent no está en la misma situación pero no aporta gran valor pues solo es el identificador de los agentes, no el nombre en si. Por tanto se procede a eliminar esas variables:
        """
    )

    # cleanData = data.drop(columns=["company", "agent"], axis=1)

    st.write(
        """
        - La columna children tiene 4 valores nulos. Se procede a eliminar las filas con valores nulos en la columna children:
        """
    )
    # cleanData1 = cleanData.dropna(subset=['country', 'children'], axis = 0)
    st.write(cleanData1.isnull().sum())

    st.write("---")
    st.write(
        """
        - Para la variable children que es numérica sería necesario analizar su simetría y luego sustituir con su media o mediana:
        """
    )

    st.pyplot(sns.displot(cleanData1["children"]))

    st.write("#### children")
    st.write("Media: ", cleanData1["children"].mean())
    st.write("Mediana: ", cleanData1["children"].median())
    st.write("Moda: ", cleanData1["children"].mode()[0])
    st.write("Asimetría: ", cleanData1["children"].skew())


    st.write(cleanData1["children"].describe())

    st.write(
        """
        - A los datos faltantes lo sustituímos por 0, porque su mediana es 0:
        """
    )

    # cleanData1["children"].replace(np.nan, 0, inplace=True)

    st.write(cleanData1.isnull().sum())




if st.session_state.page == 'tipos':

    st.title('Tipos de datos')

    st.write(
        """
        La columna children tiene como tipo de dato float, pero debería ser int, entonces procedemos a cambiarle su tipo de dato, lo mismo hacemos para la columna reservation_status_date lo cambiamos de tipo object a DateTime:
        """
    )


    # # Cambiar el tipo de dato de la columna children a int
    # cleanData1["children"] = cleanData1["children"].astype(int)
    # # Cambiar el tipo de dato de la columna reservation_status_date a DateTime
    # cleanData1["reservation_status_date"] = pd.to_datetime(cleanData1["reservation_status_date"])

    st.write(cleanData1.dtypes)



if st.session_state.page == 'inconsistentes':
    
        st.title('Datos inconsistentes')
        st.write("### Datos inconsistentes")
    
        st.write(
            """
            - Al analizar las caracteristicas de las reservas, en concreto en lo que se refiere a los huéspedes, se puede observar que existen registros que cumplen con la condición de que: `(data.children == 0) & (data.adults == 0) & (data.babies == 0)`
            
            - No puede haber O’s en una misma observación en adults, children y babies (no se puede hacer una reserva sin huéspedes).

            - Estos registros se deben eliminar:
            """
        )
    
        st.write(
            """
            - La columna adr tiene valores negativos, lo cual no tiene sentido en el contexto de la tarifa diaria. Se procede a eliminar las filas con valores negativos en la columna adr:
            """
        )
    
        # Eliminar las filas con (data.children == 0) & (data.adults == 0) & (data.babies == 0)
        # inconsistentData = cleanData1[(cleanData1["children"] != 0) | (cleanData1["adults"] != 0) | (cleanData1["babies"] != 0)]
        
        st.write("**Cantidad de datos con adults, children y babies igual a 0 en la misma reserva es:** ", inconsistentData.shape[0])

        st.write("Se concluye que se trata de un error, por lo que se procede a eliminarlos", consistentData.shape)

        st.write("---")
        
        st.write("Comprobación de que no hay registros que sumen cero y por tanto el número de registros total es correcto:")
        
        #Total de huéspedes:
        localData = consistentData.copy()
        localData["Total_Guests"] = consistentData["adults"] + consistentData["children"]
    
        #Comprobamos que efectivamente no hay ningún registro que sume 0:
        filter = localData.Total_Guests != 0
        st.write("Imprimimos la cantidad de datos cuya suma sea igual a 0: ", len(filter), " donde se puede observar que no hay ningún registro que sume 0")



if st.session_state.page == 'atipicos':
    st.title('Datos atípicos')

    st.write(
        """
        Se comienza con la detección de outliers visualizando los boxplot de las diferentes variables que conforman nuestro modelo. De su visualización obtenemos un total de 8 variables que presentan cierta problemática: ‘lead time’, ‘stays in weekend nights’, ‘stays in week nights, ‘adults’, “babies’, ‘required car parking spaces’, ‘adr, ‘previous cancellations’.
        """
    )

    columnas = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults',
            'babies', 'required_car_parking_spaces', 'adr', 'previous_cancellations']
    
    st.write(
        """
        - A continuación se muestran los boxplot de las variables con outliers:
        """
    )
    
    fig, ax = plt.subplots(4, 2, figsize=(15, 15))
    fig.suptitle('Boxplot de las variables con outliers')
    for i, col in enumerate(columnas):
        sns.boxplot(data=consistentData, x=col, ax=ax[i//2, i%2])
    st.pyplot(fig)

    st.write("---")

    st.write(
        """
        - A continuación, Se procede a sustituir la mayoria de los valores atípicos por otros dentro del último cuartil o por el valor cero dependiendo del caso.:
        """
    )

    # Sustituir los valores atípicos de la columna lead_time por el valor del último cuartil
    q3 = consistentData["lead_time"].quantile(0.75)
    consistentData["lead_time"] = np.where(consistentData["lead_time"] > q3, q3, consistentData["lead_time"])

    # Sustituir los valores atípicos de las columnas stays_in_weekend_nights y stays_in_week_nights por 0
    consistentData["stays_in_weekend_nights"] = np.where(consistentData["stays_in_weekend_nights"] > 0, 0, consistentData["stays_in_weekend_nights"])
    consistentData["stays_in_week_nights"] = np.where(consistentData["stays_in_week_nights"] > 0, 0, consistentData["stays_in_week_nights"])

    # Sustituir los valores atípicos de la columna adults por el valor del último cuartil
    q3 = consistentData["adults"].quantile(0.75)
    consistentData["adults"] = np.where(consistentData["adults"] > q3, q3, consistentData["adults"])

    # Sustituir los valores atípicos de la columna babies por 0
    consistentData["babies"] = np.where(consistentData["babies"] > 0, 0, consistentData["babies"])

    # Sustituir los valores atípicos de la columna required_car_parking_spaces por 0
    consistentData["required_car_parking_spaces"] = np.where(consistentData["required_car_parking_spaces"] > 0, 0, consistentData["required_car_parking_spaces"])

    # Sustituir los valores atípicos de la columna adr por el valor del último cuartil
    q3 = consistentData["adr"].quantile(0.75)
    consistentData["adr"] = np.where(consistentData["adr"] > q3, q3, consistentData["adr"])

    # Sustituir los valores atípicos de la columna previous_cancellations por 0
    consistentData["previous_cancellations"] = np.where(consistentData["previous_cancellations"] > 0, 0, consistentData["previous_cancellations"])

    st.write(
        """
        - Se procede a visualizar nuevamente los boxplot de las variables con outliers:
        """
    )

    fig, ax = plt.subplots(4, 2, figsize=(15, 15))
    fig.suptitle('Boxplot de las variables con outliers')
    for i, col in enumerate(columnas):
        sns.boxplot(data=consistentData, x=col, ax=ax[i//2, i%2])
    st.pyplot(fig)


    st.write("---")


    st.write(
        """
        - Analizaremos todas las variables para saber si hay registros atípicos e inconsistentes entre ellas, se usará el algoritmo de LOF. Para el ejemplo se utiliza una selección de las variables numéricas
        """
    )

    #Seleccionar columnas:
    select_df = consistentData[['lead_time', 'arrival_date_year', 'stays_in_weekend_nights', 'adults',
                'is_repeated_guest', 'previous_cancellations', 'required_car_parking_spaces',
                'adr']]

    #Especificar el modelo que se va a utilizar:
    model = LocalOutlierFactor(n_neighbors = 30)

    #Ajuste al modelo:
    y_pred = model.fit_predict(select_df)

    #Filtrar los indices de los outliers
    outlier_index = (y_pred == - 1) #los valores negativos son outliers
    
    #Filtrar los valores de los outliers en el dataframe
    outlier_values = select_df.iloc[outlier_index]
    

    st.write(
        """
            1. Seleccionamos las columnas numéricas, que son: 'lead_time', 'arrival_date_year', 'stays_in_weekend_nights', 'adults', 'is_repeated_guest', 'previous_cancellations', 'required_car_parking_spaces', 'adr'.
            2. Se especifica el modelo que se va a utilizar, en este caso se utiliza el algoritmo de LOF.
            3. Se ajusta el modelo, y se predice los valores.
            4. Se filtran los indices de los outliers, los valores negativos son outliers.
            5. Se filtran los valores de los outliers en el dataframe.
        """
    )

    st.write("### Outliers")

    #Imprimir los valores de los outliers
    st.write("Se muestran  la cantidad de outliers en el dataframe: ", outlier_values.shape)

    st.write("Si se aplica una técnica basado en distancias, es importante eliminar los datos atípicos, pero en este caso no se eliminarán los outliers, ya que se considera que son datos válidos, viendo sus variaciones")


if st.session_state.page == 'redundantes':
    st.title('Datos redundantes')

    st.write(
        """
        - Para identificar los atributos redundantes se pueden utilizar la matriz de correlación e indentificar correlaciones entre atributos.
        - La matriz de correlación solo se calcula sobre atributos numéricos.
        """
    )

    st.write(
        """
        - Se procede a calcular la matriz de correlación de las variables numéricas:
        """
    )

    # Selección de las variables numéricas
    numeric_columns = consistentData.select_dtypes(include=[np.number])

    fig = plt.figure(figsize = (24, 12))
    # Calcular la matriz de correlación
    correlation = numeric_columns.corr()

    # Visualizar la matriz de correlación
    sns.heatmap(correlation, annot = True, linewidths = 1)
    st.pyplot(fig)



if st.session_state.page == 'duplicados':
    st.title('Datos duplicados')

    st.write("El anális de datos duplicados en este conjunto es interesante")
    st.write(
        """
        - Existen muchas filas duplicadas, sin embargo en algunos casos pudieran ser coincidencias de reservas iguales, para clientes diferentes.
        - En este caso es mejor indagar un poco en el negocio para saber cual es realmente la posibilidad de reservas identicas.
        - En último recursos, si se eliminan todos los duplicados, quedarían aún suficientes datos para realizar un análisis interesante.
        """
    )

    # Detección de datos duplicados
    duplicated_data = consistentData[consistentData.duplicated()]

    st.write("### Datos duplicados")
    st.write("Cantidad de datos duplicados: ", duplicated_data.shape[0])

    st.write("### Ver las filas duplicadas")
    st.write(duplicated_data)