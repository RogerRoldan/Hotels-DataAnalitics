import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
data_url = 'data/hotel_bookings.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(data_url)
    return data

# Configurar el estado de la página
def set_page(page):
    st.session_state.page = page
    st.experimental_rerun()

def main():
    st.title("Análisis de Reservas de Hotel")

    # Cargar los datos
    data = load_data()

    # Filtros
    hotel_type = st.selectbox("Tipo de Hotel", data['hotel'].unique())
    country = st.selectbox("País de Origen", data['country'].unique())
    market_segment = st.selectbox("Tipo de Reserva", data['market_segment'].unique())
    customer_type = st.selectbox("Tipo de Cliente", data['customer_type'].unique())
    month = st.selectbox("Mes del Año", data['arrival_date_month'].unique())

    # Filtrar los datos
    filtered_data = data[
        (data['hotel'] == hotel_type) &
        (data['country'] == country) &
        (data['market_segment'] == market_segment) &
        (data['customer_type'] == customer_type) &
        (data['arrival_date_month'] == month)
    ]

    # Crear la gráfica
    fig, ax = plt.subplots()
    ax.hist(filtered_data['is_canceled'], bins=3, edgecolor='black')
    ax.set_title('Cancelaciones de Reservas')
    ax.set_xlabel('Cancelado')
    ax.set_ylabel('Número de Reservas')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['No', 'Sí'])

    st.pyplot(fig)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = 'main'
    
    if st.session_state.page == 'main':
        main()
