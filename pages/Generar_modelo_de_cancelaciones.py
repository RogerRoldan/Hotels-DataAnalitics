import streamlit as st
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data_url = 'data/hotel_bookings.csv'

# Cargar los datos
@st.cache_data
def load_data():
    data = pd.read_csv(data_url)
    return data

def train_model():
    st.title("Entrenamiento del modelo de predicción de cancelaciones")

    # Cargar datos
    data = load_data()

    # Seleccionar las columnas relevantes
    X = data[['lead_time', 'arrival_date_month', 'adults', 'customer_type']]
    y = data['is_canceled']

    # Convertir columnas categóricas a variables dummy
    X = pd.get_dummies(X, columns=['arrival_date_month', 'customer_type'], drop_first=True)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Guardar el modelo y las columnas
    with open('cancellation_model.pkl', 'wb') as file:
        pickle.dump({'model': model, 'columns': X_train.columns.tolist()}, file)

    st.success("Modelo entrenado y guardado exitosamente.")

if __name__ == "__main__":
    train_model()
