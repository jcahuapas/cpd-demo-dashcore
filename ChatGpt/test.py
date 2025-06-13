from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd

# Supongamos que tienes un DataFrame con información sobre atención a animales en la veterinaria
data = {
    'Animal': ['Perro'] * 100 + ['Gato'] * 50 + ['Otro'] * 30,
    'Sintoma': ['Fiebre', 'Vómitos', 'Diarrea', 'Fiebre', 'Tos', 'Dolor', 'Fiebre', 'Vómitos', 'Dolor'] * 20,
}

df = pd.DataFrame(data)

# Cargar plantillas
templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)

# Crear figura
fig = px.histogram(df, x="Sintoma", title="Síntomas más comunes en Perros",
                   labels={'Sintoma': 'Síntoma', 'count': 'Cantidad'})

# Configurar diseño y tema
fig.update_layout(
    xaxis_title="Síntoma",
    yaxis_title="Cantidad",
    template="plotly",
)

# Configurar estilo del histograma
fig.update_traces(marker_color='#008B8B', marker_line_color='#000000', marker_line_width=0.5)

# Crear aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Diseño de la aplicación
app.layout = dbc.Container([
    dcc.Graph(figure=fig, className="m-4")
])



if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.10", port=8050)   
