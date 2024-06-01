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


st.set_page_config(page_title="Resultados", page_icon="✅")

st.title('Resultados')
st.write('Contenido sobre los resultados.')

# Cargar los datos
data_url = 'data/hotel_bookings.csv'

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(data_url)


# Cargar el modelo entrenado
model = joblib.load('modelo_prediccion_solicitudes.pkl')


# Inputs del usuario para probar el modelo
st.write("### Prueba el modelo con tus propios datos")

# Inputs simplificados del usuario
lead_time = st.number_input('Lead Time (días entre la reserva y la llegada)', min_value=0, max_value=365, value=0)
stays_in_weekend_nights = st.number_input('Noches de fin de semana', min_value=0, max_value=14, value=0)
stays_in_week_nights = st.number_input('Noches entre semana', min_value=0, max_value=14, value=0)
adults = st.number_input('Número de adultos', min_value=1, max_value=4, value=1)
children = st.number_input('Número de niños', min_value=0, max_value=4, value=0)
babies = st.number_input('Número de bebés', min_value=0, max_value=4, value=0)
booking_changes = st.number_input('Cambios en la reserva', min_value=0, max_value=20, value=0)

# Definir un umbral para considerar un número alto de solicitudes especiales
df['high_special_requests'] = df['total_of_special_requests'] > 2  # Ejemplo: más de 2 solicitudes especiales

# Preparar los datos para el modelo
X = df.drop(['total_of_special_requests', 'high_special_requests'], axis=1)
X = pd.get_dummies(X, drop_first=True)
y = df['high_special_requests']


# Botón para predecir
if st.button('Predecir'):
    # Convertir los inputs del usuario a un dataframe
    user_input_data = {
        'lead_time': lead_time,
        'stays_in_weekend_nights': stays_in_weekend_nights,
        'stays_in_week_nights': stays_in_week_nights,
        'adults': adults,
        'children': children,
        'babies': babies,
        'booking_changes': booking_changes
    }

    user_input_df = pd.DataFrame(user_input_data, index=[0])

    # Asegurar que las variables categóricas están codificadas como en el modelo
    user_input_df = pd.get_dummies(user_input_df)
    missing_cols = set(X.columns) - set(user_input_df.columns)
    for col in missing_cols:
        user_input_df[col] = 0
    user_input_df = user_input_df[X.columns]  # Asegurar el orden correcto de las columnas

    # Hacer la predicción
    user_pred = model.predict(user_input_df)
    user_pred_proba = model.predict_proba(user_input_df)

    # Mostrar los resultados
    st.write(f"**¿Alta probabilidad de solicitudes especiales?** {'Sí' if user_pred[0] else 'No'}")
    st.write(f"**Probabilidad:** {user_pred_proba[0][1]:.2f}")