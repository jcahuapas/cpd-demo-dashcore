# dash imports
from utils.file_operation import read_file_as_str
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import random
import numpy as np
import locale
from calendar import month_abbr
from maindash import my_app,color_in_graf_global,color_out_graf_global

# Configurar la localización a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


# file imports
# from maindash import my_app


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
servicios_especializados = ['Rehabilitación Física',
                            'Odontología', 'Dermatología', 'Cardiología', 'Nutrición']
porcentaje_servicios_especializados = np.random.rand(5) * 100

# Color personalizado para los valores
colores_valores_pie = ['#E49835', '#7E808F', '#F44336', '#607CA5', '#B5A7C0']


######
# id='ingresos-servicios' - Inicio
######
# Crear gráfico de barras y líneas para ingresos de servicios
fig_ingresos_servicios = go.Figure()

# Agregar barras para ingresos de servicios
for i in range(3):
    if i == 0:
        C_COLOR = "#7E808F"
    elif i == 1:
        C_COLOR = "#A598AF"
    elif i == 2:
        C_COLOR = "#607CA5"

    fig_ingresos_servicios.add_trace(go.Bar(
        x=list(range(1, 13)),
        y=ingresos_servicios[i],
        name=servicios[i],
        marker_color=C_COLOR)
    )

# Agregar líneas para el promedio
for i in range(1):
    fig_ingresos_servicios.add_trace(go.Scatter(
        x=list(range(1, 13)),
        y=[np.mean(ingresos_servicios[i])] * 12,
        mode='lines',
        name=f'Promedio - {servicios[i]}',
        # Cambiar colores según tus preferencias
        line=dict(color=f'rgba({i * 50}, {i * 100}, {i * 25}, 0.8)')
    ))

# Actualizar diseño del gráfico
fig_ingresos_servicios.update_layout(
    title='<b>Fuentes de Ingresos por Servicio</b>',
    # xaxis=dict(title='Mes'),
    xaxis=dict(title='Mes', tickvals=list(
        range(1, 13)), ticktext=month_abbr[1:]),
    yaxis=dict(title='Ingresos'),
    barmode='stack',
    paper_bgcolor = color_out_graf_global,
    plot_bgcolor = color_in_graf_global,
)
######
# id='ingresos-servicios' - Fin
######
######
# id='costos-operativos' - Inicio
######
# Supongamos que tienes una lista de colores que quieres usar para las líneas.
colores = ['#E49835', '#F44336', '#7E808F']

# Supongamos que tienes una lista de nombres para las series.
nombres_series = ['Personal', 'Suministros', 'Equipamiento']

# Supongamos que tienes una lista de datos para y (costos_valores).
costos_valores = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                  [2, 4, 1, 6, 8, 3, 5, 7, 9, 4, 8, 12],
                  [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]]

# Crear el objeto de figura
fig_costos_servicios = {
    'data': [go.Scatter(x=list(range(1, 13)), y=costos_valores[i], mode='lines+markers', name=nombres_series[i],
                        line={'color': colores[i]}) for i in range(3)],
    'layout': go.Layout(title='<b>Costos Operativos</b>',
                        xaxis=dict(title='Mes', 
                        tickvals=list(range(1, 13)), 
                        ticktext=month_abbr[1:]),
                        paper_bgcolor = color_out_graf_global,
                        plot_bgcolor = color_in_graf_global
                        )
}
######
# id='costos-operativos' - Fin
######
######
# id='fig' - Inicio
######
fig = go.Figure()

# Datos de ejemplo
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
visitas_tendencia = [1.5, 1, 1.3, 0.7, 0.8, 0.9]
visitas_barras = [1, 0.5, 0.7, -1.2, 0.3, 0.4]

# Línea para mostrar la tendencia general de las visitas
fig.add_trace(go.Scatter(
    x=meses,
    y=visitas_tendencia,
    mode='lines+markers',
    name='Tendencia General',
    line=dict(color='#607CA5')
))

# Barras para destacar meses con número negativo de visitas
fig.add_trace(go.Bar(
    x=meses,
    y=visitas_barras,
    name='Meses Negativos',
    marker=dict(color='#A598AF')
))

# Diseño del gráfico
fig.update_layout(
    title='<b>Número de Visitas a la Veterinaria</b>',
    xaxis=dict(title='Meses'),
    yaxis=dict(title='Número de Visitas'),
    showlegend=True,
    paper_bgcolor = color_out_graf_global,
    plot_bgcolor = color_in_graf_global
)
######
# id='fig' - Inicio
######
######
# id='fig_2' - Fin
######
fig_2 = go.Figure()

# Datos de ejemplo
meses = ['Enero', 'Febrero', 'Marzo', 'Abril']
crecimiento_mensual = [0, 2, 3, 5]

# Gráfico de área para representar la tasa de crecimiento mensual
fig_2.add_trace(go.Scatter(
    x=meses,
    y=crecimiento_mensual,
    mode='lines',
    fill='tozeroy',  # Rellenar hacia el eje y=0
    #name='Tasa de Crecimiento Mensual',
    line=dict(color='#D6D6D2')
))

# Diseño del gráfico
fig_2.update_layout(
    title='<b>Tasa de Crecimiento de Clientes Mensual</b>',
    xaxis=dict(title='Meses'),
    yaxis=dict(title='Tasa de Crecimiento'),
    showlegend=True,
    paper_bgcolor = color_out_graf_global,
    plot_bgcolor = color_in_graf_global    
)
######
# id='fig_2' - Fin
######

#######################################
# Layout
#######################################


def finanzas_layout():
    layout = html.Div([
        html.Div([html.H2("Finanzas"),
                  html.Img(src="..\\assets\\img\\stock-icon_.png")                  
                  ], className="banner"),
        # Primer Fila
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='ingresos-servicios',
                    figure=fig_ingresos_servicios
                )
            ),
        ]),
        html.Br(),
        # Segunda Fila
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='costos-operativos',
                    figure=fig_costos_servicios
                )
            ),
        ]),
        html.Br(),
        # Tercera Fila
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='analisis-rentabilidad-clientes',
                    figure={
                        'data': [go.Scatter(x=list(range(1, 7)), y=ingresos_clientes[i], mode='markers', name=clientes[i]) for i in range(20)],
                        'layout': go.Layout(title='<b>Análisis de Rentabilidad por Cliente</b>',
                                            paper_bgcolor = color_out_graf_global,
                                            plot_bgcolor = color_in_graf_global
                                            )
                    }
                )
            ),
            dbc.Col(
                dcc.Graph(
                    id='porcentaje-servicios-especializados',
                    figure={
                        'data': [go.Pie(labels=servicios_especializados, values=porcentaje_servicios_especializados, hole=0.4,
                     hoverinfo="label+percent", marker=dict(colors=colores_valores_pie))],
                        'layout': go.Layout(title='<b>Porcentaje de Ingresos por Servicios Especializados</b>', 
                                            paper_bgcolor = color_out_graf_global,
                                            plot_bgcolor = color_in_graf_global
                                            ),
                    }
                )
            ),
        ]),  
        html.Br(),      
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='fig',
                    figure=fig
                )
            ),
            dbc.Col(
                dcc.Graph(
                    id='fig_2',
                    figure=fig_2,                    
                )
            ),
        ]),
    ]),
    return layout
