import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib


st.set_page_config(page_title="Analizando los datos", page_icon="📈")
st.title('Analizar los Datos')

# Cargar los datos
data_url = 'data/hotel_bookings.csv'

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(data_url)


st.write("---")


# Definir el orden de los meses
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Convertir 'arrival_date_month' a un tipo categórico con el orden especificado
df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)


# Pregunta 1: Mejor época del año para reservar una habitación de hotel
st.write("### Mejor época del año para reservar una habitación de hotel")
monthly_adr = df.groupby('arrival_date_month')['adr'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=monthly_adr, x='arrival_date_month', y='adr', ax=ax, order=month_order)
ax.set_title('Tarifa Diaria Promedio por Mes')
ax.set_xlabel('Mes de llegada')
ax.set_ylabel('Tarifa Diaria Promedio (ADR)')
st.pyplot(fig)


st.write(
    """
    Nuestro análisis revela que la demanda de habitaciones de hotel varía significativamente a lo largo del año. Observamos picos de reservas durante los meses de verano y las vacaciones de invierno, con tarifas más altas debido a la alta demanda. Por otro lado, las temporadas bajas, como el inicio del año y el otoño, presentan menores volúmenes de reservas y tarifas más bajas. Por lo tanto, la mejor época para reservar una habitación de hotel, en términos de costo y disponibilidad, sería durante la temporada baja, cuando las tarifas son más competitivas y hay mayor disponibilidad de habitaciones
    """
)


st.write("---")



# lIMPIEZA DE DATOS
# Eliminar los valores nulos de las columnas company, agent y children
cleanData = df.drop(columns=["company", "agent"], axis=1)
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



columnas = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults',
            'babies', 'required_car_parking_spaces', 'adr', 'previous_cancellations']

# Sustituir los valores atípicos de la columna adr por el valor del último cuartil
q3 = consistentData["adr"].quantile(0.75)
consistentData["adr"] = np.where(consistentData["adr"] > q3, q3, consistentData["adr"])

# Pregunta 2: Duración óptima de la estancia para obtener la mejor tarifa diaria
st.write("### Duración óptima de la estancia para obtener la mejor tarifa diaria")
df['total_stays'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
stay_adr = df.groupby('total_stays')['adr'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=stay_adr, x='total_stays', y='adr', ax=ax)
ax.set_title('Tarifa Diaria Promedio por Duración de la Estancia')
ax.set_xlabel('Duración de la Estancia (días)')
ax.set_ylabel('Tarifa Diaria Promedio (ADR)')
ax.set_xlim(0, 50)  # Establecer el límite del eje x entre 0 y 50   
st.pyplot(fig)


st.write(
    """
    Nuestro análisis sugiere que la duración óptima de la estancia para obtener la mejor tarifa diaria es de 1 a 4 días. Las tarifas diarias tienden a disminuir a medida que aumenta la duración de la estancia, con una tendencia a estabilizarse después de 4 días. Por lo tanto, para obtener la mejor tarifa diaria, se recomienda una estancia de corta duración, idealmente entre 1 y 4 días.
    """
)


# st.write("---")


# st.write(
#   """
#     Para abordar esta pregunta, construimos un modelo predictivo utilizando variables relevantes, como el tipo de cliente, la duración de la estancia y el tipo de habitación, entre otros factores, para predecir la probabilidad de recibir solicitudes especiales.

#     Nuestro modelo de clasificación se basa en un algoritmo de bosque aleatorio (Random Forest), que es capaz de manejar múltiples variables y relaciones complejas entre ellas. Utilizamos una métrica de evaluación como la precisión (accuracy) para medir el rendimiento del modelo en la predicción de solicitudes especiales.
#   """
# )
# # Pregunta 3: Predicción de solicitudes especiales
# st.write("### Predicción de solicitudes especiales")

# # Definir un umbral para considerar un número alto de solicitudes especiales
# df['high_special_requests'] = df['total_of_special_requests'] > 2  # Ejemplo: más de 2 solicitudes especiales

# # Preparar los datos para el modelo
# X = df.drop(['total_of_special_requests', 'high_special_requests'], axis=1)
# X = pd.get_dummies(X, drop_first=True)
# y = df['high_special_requests']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Entrenar un modelo de clasificación
# model = RandomForestClassifier()
# model.fit(X_train, y_train)


# # Guardar el modelo entrenado
# joblib.dump(model, 'modelo_prediccion_solicitudes.pkl')

# y_pred = model.predict(X_test)

# accuracy = accuracy_score(y_test, y_pred)
# report = classification_report(y_test, y_pred, output_dict=True)

# st.write(f"**Accuracy del modelo:** {accuracy:.2f}")
# st.write("**Reporte de clasificación:**")
# st.dataframe(pd.DataFrame(report).transpose())




# # Inputs del usuario para probar el modelo
# st.write("### Prueba el modelo con tus propios datos")

# # Inputs simplificados del usuario
# lead_time = st.number_input('Lead Time (días entre la reserva y la llegada)', min_value=0, max_value=365, value=0)
# stays_in_weekend_nights = st.number_input('Noches de fin de semana', min_value=0, max_value=14, value=0)
# stays_in_week_nights = st.number_input('Noches entre semana', min_value=0, max_value=14, value=0)
# adults = st.number_input('Número de adultos', min_value=1, max_value=4, value=1)
# children = st.number_input('Número de niños', min_value=0, max_value=4, value=0)
# babies = st.number_input('Número de bebés', min_value=0, max_value=4, value=0)
# booking_changes = st.number_input('Cambios en la reserva', min_value=0, max_value=20, value=0)

# # Botón para predecir
# if st.button('Predecir'):
#     # Convertir los inputs del usuario a un dataframe
#     user_input_data = {
#         'lead_time': lead_time,
#         'stays_in_weekend_nights': stays_in_weekend_nights,
#         'stays_in_week_nights': stays_in_week_nights,
#         'adults': adults,
#         'children': children,
#         'babies': babies,
#         'booking_changes': booking_changes
#     }

#     user_input_df = pd.DataFrame(user_input_data, index=[0])

#     # Asegurar que las variables categóricas están codificadas como en el modelo
#     user_input_df = pd.get_dummies(user_input_df)
#     missing_cols = set(X.columns) - set(user_input_df.columns)
#     for col in missing_cols:
#         user_input_df[col] = 0
#     user_input_df = user_input_df[X.columns]  # Asegurar el orden correcto de las columnas

#     # Hacer la predicción
#     model.fit(X_train, y_train)
#     user_pred = model.predict(user_input_df)
#     user_pred_proba = model.predict_proba(user_input_df)

#     # Mostrar los resultados
#     st.write(f"**¿Alta probabilidad de solicitudes especiales?** {'Sí' if user_pred[0] else 'No'}")
#     st.write(f"**Probabilidad:** {user_pred_proba[0][1]:.2f}")