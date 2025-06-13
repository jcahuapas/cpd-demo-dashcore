import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import random

####### PROMPT Chat-GPT################
# Chat-GPT
# genera un script usando plotly.graph_objects y dash-bootstrap-components que muestra los siguientes indicadores 
# usa from dash import html
# usa from dash import dcc

# 1.- En la primer fila, genera un indicador con la venta total de la semana, y que muesyte un % positivo a la semana anterior 
# 2.- En la primer fila, genera un indicador con Total de Atencion de la semana, y que muesyte un % positivo a la semana anterior

# 3.- En la primer fila, genera un grafico tipo donut lado de las cards, este grafico debe mostrar un % de cumplomiento (dato aleatorio) y que muestre un monto en Miles (dato aleatorio) en el centro del donuts, de la Ganancia Bruta del Mes (misma altura que los 2 primeros graficos)

# 4.- en una segunda fila, agregar un grafico tipo linea con la evolucion de Venta de Medicamentes por dia, de un mes (datos aleatorio) (markets and line)

# 5.- en la seguna dila , agregar un grafico de barras, donde muestre la cantidad de subscritores en Instagram, (datos aleatorio en Miles), cada 5 dias de un mes (eje x). En el Eje Y debe mostrar un color de barra positivo (Nuevos subscribtores), 
# tambien en el mismo eje Y negativo debe mostrar otro color de barra para los datos Negativos (cantidad de dessubscripciones). visualizar la data en eje Y negativo base=[]
#######################

# Generar datos de ejemplo aleatorios
venta_total_semana = random.randint(5000, 10000)
total_atencion_semana = random.randint(2000, 8000)
cumplimiento_porcentaje = random.uniform(80, 100)
ganancia_bruta_miles = random.randint(50000, 100000)

# Datos de ejemplo para la evolución de ventas de medicamentos por día
dias_mes = list(range(1, 31))
ventas_medicamentos_diarias = [random.randint(50, 200) for _ in dias_mes]

# Datos de ejemplo para la evolución de suscriptores en Instagram cada 5 días
dias_subscriptores = list(range(1, 31, 5))
nuevos_subscriptores = [random.randint(100, 500) for _ in range(len(dias_subscriptores))]
desuscripciones = [random.randint(0, 100) for _ in range(len(dias_subscriptores))]

# Crear gráfico de líneas para la evolución de ventas de medicamentos por día
fig_ventas_medicamentos = go.Figure()
fig_ventas_medicamentos.add_trace(go.Scatter(x=dias_mes, y=ventas_medicamentos_diarias, mode='lines+markers', name='Ventas Medicamentos'))
fig_ventas_medicamentos.update_layout(title='Evolución de Ventas de Medicamentos por Día', xaxis=dict(title='Día'), yaxis=dict(title='Cantidad'))

# Crear gráfico de barras para suscriptores en Instagram
fig_subscriptores = go.Figure()
fig_subscriptores.add_trace(go.Bar(x=dias_subscriptores, y=nuevos_subscriptores,base=[], name='Nuevos Subscriptores', marker_color='rgba(71, 134, 81, 0.8)'))
fig_subscriptores.add_trace(go.Bar(x=dias_subscriptores, y=[-x for x in desuscripciones], name='Desuscripciones', marker_color='rgba(219, 64, 82, 0.8)'))
fig_subscriptores.update_layout(title='Evolución de Suscriptores en Instagram', xaxis=dict(title='Día'), yaxis=dict(title='Cantidad'), barmode='stack')

# Configurar la aplicación Dash con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Diseño del tablero con los indicadores y gráficos
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Venta Total Semana", className="card-title"),
                    html.P(f"${venta_total_semana:,.2f}", className="card-text"),
                    html.P("Semana Anterior: +5%", className="card-text text-success")
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Atención Semana", className="card-title"),
                    html.P(f"${total_atencion_semana:,.2f}", className="card-text"),
                    html.P("Semana Anterior: +8%", className="card-text text-success")
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='donut-chart', figure={
                        'data': [go.Pie(labels=['Cumplimiento', 'Restante'], values=[cumplimiento_porcentaje, 100 - cumplimiento_porcentaje],
                                       hole=0.7, marker_colors=['rgba(71, 134, 81, 0.8)', 'rgba(200, 200, 200, 0.8)'])],
                        'layout': go.Layout(title='Cumplimiento de Objetivos', height=250)
                    }),
                ])
            ]),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='ventas-medicamentos-chart', figure=fig_ventas_medicamentos),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='subscriptores-chart', figure=fig_subscriptores)
        ], width=6)
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.9", port=8050)   
