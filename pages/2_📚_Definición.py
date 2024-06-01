import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Definición", page_icon="📚")

st.markdown("# Comprendamos el negocio acerca de la demanda de reserva de hotel")
st.sidebar.header("Demanda de reserva de hotel")
st.write(
    """En esta sección se describe el problema de predicción de la demanda de reserva de hotel, indicando el contexto del problema, y los datos utilizados"""
)

st.markdown("## Contexto")
st.write(
    """
    #### Alguna vez te has preguntado... 🤔

     * ¿Cuál es la mejor época del año para reservar una habitación de hotel? 
     * ¿La duración óptima de la estancia para obtener la mejor tarifa diaria? 
     * ¿Qué pasaría si quisiera predecir si es probable que un hotel reciba o no un número desproporcionadamente alto de solicitudes especiales?
    """
)

st.markdown("## Contenido")
st.write(
    """
    ¡Este conjunto de datos de reservas de hotel puede ayudarle a explorar esas preguntas!

    Este conjunto de datos contiene información de reserva para un hotel urbano y un hotel resort, e incluye información como cuándo se realizó la reserva, duración de la estancia, número de adultos, niños y/o bebés, y número de plazas de aparcamiento disponibles. entre otras cosas.

    * Cada fila consiste en una reserva del hotel.
    * Incluye información sobre cuando fue realizada.
    * La duración de la estadía.
    * El número de adultos, niños y bebés entre otras cosas.

    Toda la información de identificación personal ha sido eliminada de los datos.

    #### Fuentes de datos
    * [Hotel Bookings](https://www.kaggle.com/jessemostipak/hotel-booking-demand)

    ---
    """
)