import streamlit as st
import pandas as pd
import pickle

def load_model():
    with open('cancellation_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data['model'], data['columns']

def predict_cancellation(model, columns, lead_time, arrival_date_month, adults, customer_type):
    input_data = pd.DataFrame({
        'lead_time': [lead_time],
        'arrival_date_month': [arrival_date_month],
        'adults': [adults],
        'customer_type': [customer_type]
    })

    input_data = pd.get_dummies(input_data, columns=['arrival_date_month', 'customer_type'], drop_first=True)
    input_data = input_data.reindex(columns=columns, fill_value=0)

    prediction = model.predict(input_data)
    return prediction[0]

def main():
    st.title("Predicción de cancelaciones de reservas")

    lead_time = st.number_input("Días entre la reserva y el check-in", min_value=0)
    arrival_date_month = st.selectbox("Mes de llegada", ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    adults = st.number_input("Número de adultos", min_value=1)
    customer_type = st.selectbox("Tipo de cliente", ['Contract', 'Group', 'Transient', 'Transient-party'])

    model, columns = load_model()

    if st.button("Predecir"):
        prediction = predict_cancellation(model, columns, lead_time, arrival_date_month, adults, customer_type)
        if prediction == 1:
            st.error("La reserva se cancelará.")
        else:
            st.success("La reserva no se cancelará.")

if __name__ == "__main__":
    main()
