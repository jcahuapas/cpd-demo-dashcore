import plotly.graph_objects as go
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np

####### PROMPT Chat-GPT################
# Chat-GPT
# genera un script usando plotly.graph_objects y dash-bootstrap-components que muestra los siguientes indicadores 
# usa from dash import html
# usa from dash import dcc

# 1.- En la primer fila, genera un grafico combinado  barras :donde pueda Examinar las fuentes de ingresos actuales de la clínica, muestra los servicios más rentables en el mismo  (usa datos aleatorios) en 12 meses. , grafico linea: linea punteada donde 
# muestre una constante promedio 
# 2.- En la segunda fila, genera un grafico de lineas con markets que refleje los costos operativos (genera 3 tipos de costos operativos) en 12 meses

# 3.- En la tercera Fila, genera un grafico de burbuja quue refleje un análisis de rentabilidad por 20 cliente para identificar a aquellos que generan mayores ingresos. Enfoca tus esfuerzos de marketing y atención en este segmento. en los ultmos 6 meses
# 4.- .- En la tercera Fila, genera un grafico de donut quue refleje Porcentaje de ingresos provenientes de servicios especializados. (Rehabilitación Física para Mascotas, Odontología Veterinaria, Dermatología Veterinaria, Cardiología Veterinaria, Nutrición Especializada para Mascotas)

# Datos aleatorios para los servicios
servicios = ['Consulta General', 'Vacunación', 'Cirugía']
ingresos_servicios = np.random.randint(1000, 5000, size=(3, 12))

# Datos aleatorios para los costos operativos
costos_operativos = ['Personal', 'Suministros', 'Equipamiento']
costos_valores = np.random.randint(500, 2000, size=(3, 12))

# Datos aleatorios para el análisis de rentabilidad por cliente
clientes = ['Cliente {}'.format(i) for i in range(1, 21)]
ingresos_clientes = np.random.randint(200, 1000, size=(20, 6))

# Datos para el porcentaje de ingresos de servicios especializados
servicios_especializados = ['Rehabilitación Física', 'Odontología', 'Dermatología', 'Cardiología', 'Nutrición']
porcentaje_servicios_especializados = np.random.rand(5) * 100

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Diseño del dashboard
app.layout = html.Div([
    # Primer Fila
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='ingresos-servicios',
                figure={
                    'data': [go.Bar(x=list(range(1, 13)), y=ingresos_servicios[i], name=servicios[i]) for i in range(3)] +
                            [go.Scatter(x=list(range(1, 13)), y=[np.mean(ingresos_servicios[i])] * 12, mode='lines', name='Promedio') for i in range(3)],
                    'layout': go.Layout(title='Fuentes de Ingresos por Servicio')
                }
            )
        ),
    ]),

    # Segunda Fila
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='costos-operativos',
                figure={
                    'data': [go.Scatter(x=list(range(1, 13)), y=costos_valores[i], mode='lines', name=costos_operativos[i]) for i in range(3)],
                    'layout': go.Layout(title='Costos Operativos')
                }
            )
        ),
    ]),

    # Tercera Fila
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='analisis-rentabilidad-clientes',
                figure={
                    'data': [go.Scatter(x=list(range(1, 7)), y=ingresos_clientes[i], mode='markers', name=clientes[i]) for i in range(20)],
                    'layout': go.Layout(title='Análisis de Rentabilidad por Cliente')
                }
            )
        ),
        dbc.Col(
            dcc.Graph(
                id='porcentaje-servicios-especializados',
                figure={
                    'data': [go.Pie(labels=servicios_especializados, values=porcentaje_servicios_especializados)],
                    'layout': go.Layout(title='Porcentaje de Ingresos por Servicios Especializados')
                }
            )
        ),
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.10", port=8050)   

