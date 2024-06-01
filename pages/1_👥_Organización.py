import streamlit as st

st.set_page_config(page_title="Organización", page_icon="👥")

st.title("Organización", help="Página de organización")
st.sidebar.header("Plotting Demo")
st.write(
    """En esta sección se describe la organización del trabajo en este proyecto de análisis de datos, indicando el grupo de trabajo, y el rol de cada uno, teniendo encuenta la metodología de trabajo CRISP-DM."""
)

st.markdown("## Grupo de trabajo")
st.write(
    """El grupo de trabajo está conformado por los siguientes integrantes:
- **Roger Ricardo Roldan Bonilla**
- **Yeferson Yuberley Guerrero Castro**"""
)

st.markdown("## Roles")
st.write(
    """Los roles de cada integrante del grupo de trabajo son los siguientes:
- **Roger Ricardo Roldan Bonilla**:  Líder del Proyecto y Científico de Datos
- **Yeferson Yuberley Guerrero Castro**: Analista de Negocios - Ingeniero de Datos
"""
)

st.markdown("## Metodología de trabajo")
st.write(
    """
    La metodología de trabajo utilizada en este proyecto es CRISP-DM, la cual se describe a continuación:

    - **1. Comprensión del negocio**: Entender los objetivos y necesidades del negocio para definir el problema y el éxito del proyecto.
    
    - **2. Comprensión de los datos**: Recolectar y familiarizarse con los datos disponibles, evaluando su calidad y relevancia.
    
    - **3. Preparación de los datos**: Limpiar y transformar los datos para prepararlos para el análisis y el modelado.
    
    - **4. Modelado**: Aplicar técnicas estadísticas y de machine learning para construir modelos que resuelvan el problema definido.
    
    - **5. Evaluación**: Evaluar los modelos para asegurar que cumplen con los objetivos del negocio y realizar ajustes si es necesario.
    
    - **6. Despliegue**: Implementar los modelos y resultados en el entorno del negocio, asegurando su integración y uso adecuado.
    """
)

st.markdown("## Tecnologías utilizadas")
st.write(
    """Las referencias utilizadas en este proyecto son las siguientes:
- **[CRISP-DM](https://www.datascience-pm.com/crisp-dm-2/) (Cross Industry Standard Process for Data Mining)**
- **[Streamlit](https://streamlit.io/) (The fastest way to build custom ML tools)**
- **[Pandas](https://pandas.pydata.org/) (Python Data Analysis Library)**
- **[Altair](https://altair-viz.github.io/) (Declarative statistical visualization library for Python)**
- **[Scikit-learn](https://scikit-learn.org/stable/) (Machine Learning in Python)**
- **[NumPy](https://numpy.org/) (The fundamental package for scientific computing with Python)**
- **[Matplotlib](https://matplotlib.org/) (Python plotting library)**
- **[Seaborn](https://seaborn.pydata.org/) (Statistical data visualization)**
- **[Plotly](https://plotly.com/python/) (Python graphing library)**
"""
)
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")