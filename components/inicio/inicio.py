# dash imports
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import random
import pathlib

import numpy as np
import pandas as pd
import math
import datetime
from datetime import datetime as dt
# file imports
# from maindash import my_app
from utils.file_operation import read_file_as_str
from maindash import my_app,color_in_graf_global,color_out_graf_global

#######################################
# Variables Globales
#######################################



#import locale
#locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

######## DATA HEADMAP - INICIO
# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv.gz"))
#print('SHAPE: '+ str(df.shape))
# Define el mapeo de reemplazo
replacements = {"Lakeview Center": "Clinica Central","Madison Center": "Clinica Sur","Surgery Center": "Clinica Norte"}

# Realiza el reemplazo en la columna "Clinic Name"
df["Clinic Name"] = df["Clinic Name"].replace(replacements)

clinic_list = df["Clinic Name"].unique()
df["Admit Source"] = df["Admit Source"].fillna("Not Identified")
admit_list = df["Admit Source"].unique().tolist()

# Date
# Format checkin Time
df["Check-In Time"] = df["Check-In Time"].apply(
    lambda x: dt.strptime(x, "%Y-%m-%d %I:%M:%S %p")
)  # String -> Datetime

# Insert weekday and hour of checkin time
df["Days of Wk"] = df["Check-In Hour"] = df["Check-In Time"]
df["Days of Wk"] = df["Days of Wk"].apply(
    lambda x: dt.strftime(x, "%A")
)  # Datetime -> weekday string

df["Check-In Hour"] = df["Check-In Hour"].apply(
    lambda x: dt.strftime(x, "%I %p")
)  # Datetime -> int(hour) + AM/PM

day_list = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

check_in_duration = df["Check-In Time"].describe()

# Register all departments for callbacks
all_departments = df["Department"].unique().tolist()
wait_time_inputs = [
    Input((i + "_wait_time_graph"), "selectedData") for i in all_departments
]
score_inputs = [Input((i + "_score_graph"), "selectedData") for i in all_departments]

###fUNCION

def generate_patient_volume_heatmap(start, end, clinic, hm_click):
    """
    :param: start: start date from selection.
    :param: end: end date from selection.
    :param: clinic: clinic from selection.
    :param: hm_click: clickData from heatmap.
    :param: admit_type: admission type from selection.
    :param: reset (boolean): reset heatmap graph if True.

    :return: Patient volume annotated heatmap.
    """
    filtered_df = df[
        #(df["Clinic Name"] == clinic) & (df["Admit Source"].isin(admit_type))
        (df["Clinic Name"] == clinic)
    ]
    filtered_df = filtered_df.sort_values("Check-In Time").set_index("Check-In Time")[
        start:end
    ]

    #x_axis = [datetime.time(i).strftime("%I %p") for i in range(24)]  # 24hr time list    
    x_axis = [f"{(i % 12) + 1:02d} {'AM' if i < 12 else 'PM'}" for i in range(24)]




    y_axis = day_list

    hour_of_day = ""
    weekday = ""
    shapes = []

    if hm_click is not None:
        hour_of_day = hm_click["points"][0]["x"]
        weekday = hm_click["points"][0]["y"]

        # Add shapes
        x0 = x_axis.index(hour_of_day) / 24
        x1 = x0 + 1 / 24
        y0 = y_axis.index(weekday) / 7
        y1 = y0 + 1 / 7

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color="#ff6347"),
            )
        ]

    # Get z value : sum(number of records) based on x, y,

    z = np.zeros((7, 24))
    annotations = []

    for ind_y, day in enumerate(y_axis):
        filtered_day = filtered_df[filtered_df["Days of Wk"] == day]
        #print('filtered_day -EJC ')
        #print(filtered_day)
        #print('x_axis -EJC ')
        #print(x_axis)       
        
        for ind_x, x_val in enumerate(x_axis):
            #print('x_val -EJC ')
            #print(x_val)
            sum_of_record = filtered_day[filtered_day["Check-In Hour"] == x_val][
                "Number of Records"
            ].sum()

            
            #print('sum_of_record -EJC ')
            #print(sum_of_record)
            z[ind_y][ind_x] = sum_of_record
            #print(z)
            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=day,
                font=dict(family="sans-serif"),
            )            

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Patient Records"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        )
    ]

    layout = dict(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )
    #print(data)
    return {"data": data, "layout": layout}



######## DATA HERADMAP -FIN 
#####################
# GRAF BURBUJA  DATA - INICIO
#####################
# Crear datos de ejemplo
data = pd.DataFrame({
    'Cantidad de Perros': [20, 30, 15, 25, 10],
    'Síntomas': ['Fiebre', 'Tos', 'Dolor Abdominal', 'Vómitos', 'Diarrea'],
    'Esperanza de Vida': [10, 12, 9, 11, 10],
    'Sucursal': ['A', 'B', 'A', 'C', 'B']
})

# Definir texto emergente y tamaño de burbuja
hover_text = []
bubble_size = []

for index, row in data.iterrows():
    hover_text.append(('Cantidad de Perros: {cantidad}<br>'+
                      'Síntomas: {sintomas}<br>'+
                      'Esperanza de Vida: {vida}<br>'+
                      'Sucursal: {sucursal}').format(cantidad=row['Cantidad de Perros'],
                                                     sintomas=row['Síntomas'],
                                                     vida=row['Esperanza de Vida'],
                                                     sucursal=row['Sucursal']))
    bubble_size.append(math.sqrt(row['Cantidad de Perros']))

data['text'] = hover_text
data['size'] = bubble_size
sizeref = 2.*max(data['size'])/(100**2)

# Crear figura
fig_burbuja = go.Figure()

for sucursal_nombre, sucursal_datos in data.groupby('Sucursal'):
    fig_burbuja.add_trace(go.Scatter(
        x=sucursal_datos['Esperanza de Vida'],
        y=sucursal_datos['Síntomas'],
        name=f'Sucursal {sucursal_nombre}',
        text=sucursal_datos['text'],
        marker_size=sucursal_datos['size'],
        mode='markers',
    ))

# Ajustar apariencia de las burbujas y diseño
fig_burbuja.update_traces(marker=dict(sizemode='area', sizeref=sizeref, line_width=2))

fig_burbuja.update_layout(
    title='<b>Síntomas y Esperanza de Vida</b>',
    yaxis=dict(title='Síntomas'),
    xaxis=dict(title='Esperanza de Vida (años)', gridcolor='white', gridwidth=2),
    paper_bgcolor = color_out_graf_global,
    plot_bgcolor = color_in_graf_global,
)
#####################
# GRAF BURBUJA  DATA - FIN
#####################



# Generar datos de ejemplo aleatorios
venta_total_semana = random.randint(5000, 10000)
total_atencion_semana = random.randint(2000, 8000)
cumplimiento_porcentaje = random.uniform(80, 100)
ganancia_bruta_miles = random.randint(50000, 100000)

# Datos de ejemplo para la evolución de ventas de medicamentos por día
dias_mes = list(range(1, 31))
ventas_medicamentos_diarias = [random.randint(300, 800) for _ in dias_mes]

# Datos de ejemplo para la evolución de suscriptores en Instagram cada 5 días
dias_subscriptores = list(range(1, 31, 5))
nuevos_subscriptores = [random.randint(100, 500)
                        for _ in range(len(dias_subscriptores))]
desuscripciones = [random.randint(0, 100)
                   for _ in range(len(dias_subscriptores))]

# Crear gráfico de líneas para la evolución de ventas de medicamentos por día
fig_ventas_medicamentos = go.Figure()
fig_ventas_medicamentos.add_trace(go.Scatter(
    x=dias_mes, y=ventas_medicamentos_diarias, mode='lines+markers', name='Ventas Medicamentos'))
# Actualizar estilo de la línea
fig_ventas_medicamentos.update_traces(
    line=dict(color='#7E808F', width=2)  # Cambia 'red' y 2 según tus preferencias
)
fig_ventas_medicamentos.update_layout(
    title='<b>Evolución de Ventas de Medicamentos por Día</b>',     
    xaxis=dict(title='Día'), 
    yaxis=dict(title='Cantidad'),
    paper_bgcolor = color_out_graf_global,
    plot_bgcolor = color_in_graf_global
    )

# Crear gráfico de barras para suscriptores en Instagram
fig_subscriptores = go.Figure()
fig_subscriptores.add_trace(go.Bar(x=dias_subscriptores, y=nuevos_subscriptores, base=[
], name='Nuevos Subscriptores', marker_color='#607CA5'))
fig_subscriptores.add_trace(go.Bar(x=dias_subscriptores, y=[
                            -x for x in desuscripciones], name='Desuscripciones', marker_color='#A598AF'))
fig_subscriptores.update_layout(title='<b>Evolución de Suscriptores en Instagram</b>', 
                                xaxis=dict(title='Día'), 
                                yaxis=dict(title='Cantidad'), 
                                barmode='stack',
                                paper_bgcolor = color_out_graf_global,
                                plot_bgcolor = color_in_graf_global,
                                )


card_sales = dbc.Card(
    [dbc.CardBody(
        [html.H2(
            [
                html.I(className="fas fa-hand-holding-usd me-3",
                       style={"fontSize": "50px", "align-self": "flex-start"}),
                html.Span(
                    [
                        "Total"
                    ],
                    style={"display": "flex", "justify-content": "flex-end",
                           "align-items": "center"}
                )
            ],
            className="text-nowrap",
            style={"display": "flex", "justify-content": "space-between",
                   "align-items": "center"}
        ),
            html.H4("$50.7K", style={"text-align": "right"}),
            html.Div(
            [
                html.I(
                    "5.8%", className="bi bi-caret-up-fill text-success"),
                " vs LW",
                # html.Div(style={"border-top": "1px solid gray"}),
            ], style={"text-align": "right"}
        ),
        ], className="border-start border-success border-4", style={"border-radius": "15px"}
    ),
    ],
    className="text-center m-1", style={"border-radius": "15px"},
)

card_new_client = dbc.Card(
    [dbc.CardBody(
        [html.H2(
            [
                html.I(className="fas fa-paw me-3",
                       style={"fontSize": "50px", "align-self": "flex-start"}),
                html.Span(
                    [
                        "Nuevos"
                    ],
                    style={"display": "flex", "justify-content": "flex-end",
                           "align-items": "center"}
                )
            ],
            className="text-nowrap",
            style={"display": "flex", "justify-content": "space-between",
                   "align-items": "center"}
        ),
            html.H4("43", style={"text-align": "right"}),
            html.Div(
            [
                html.I(
                    "10%", className="bi bi-caret-up-fill text-success"),
                " vs LW",
                # html.Div(style={"border-top": "1px solid gray"}),
            ], style={"text-align": "right"}
        ),
        ], className="border-start border-success border-4", style={"border-radius": "15px"}
    ),
    ],
    className="text-center m-1", style={"border-radius": "15px"},
)


card_cirugias = dbc.Card(
    [dbc.CardBody(
        [html.H2(
            [
                html.I(className="fas fa-user-clock me-3",
                       style={"fontSize": "50px", "align-self": "flex-start"}),
                html.Span(
                    [
                        "Espera"
                    ],
                    style={"display": "flex", "justify-content": "flex-end",
                           "align-items": "center"}
                )
            ],
            className="text-nowrap",
            style={"display": "flex", "justify-content": "space-between",
                   "align-items": "center"}
        ),
            html.H4("28 min.", style={"text-align": "right"}),
            html.Div(
            [
                html.I(
                    "40%", className="bi bi-caret-up-fill text-danger"),
                " mas de la Media",
                # html.Div(style={"border-top": "1px solid gray"}),
            ], style={"text-align": "right"}
        ),
        ], className="border-start border-danger border-4", style={"border-radius": "15px"}
    ),
    ],
    className="text-center m-1", style={"border-radius": "15px"},
)
# PARA GUIARME CON OTRO INDICADOR
# card_new_client_2 = dbc.Card(
#     [
#         dbc.CardFooter(html.Div([
#             html.I(className="fas fa-paw me-3",
#                    style={"fontSize": "18px"}),
#             # html.Span("Venta Semanal", style={"fontSize": "14px", "verticalAlign": "middle"})
#             html.Span("Clientes ", className="mycard-header")
#         ]),
#         ),
#         dbc.CardBody(
#             [
#                 html.H2(["Nuevos"], className="text-nowrap"),
#                 html.H4("43"),
#                 html.Div(
#                     [
#                         html.I(
#                             "10%", className="bi bi-caret-up-fill text-success"),
#                         " vs LW",
#                     ]
#                 ),
#             ], className="border-start border-success border-4", style={"border-radius": "15px"}
#         ),
#     ],
#     className="text-center m-1", style={"border-radius": "15px"},
# )

#    dbc.CardFooter(html.Div([
# html.I(className="fas fa-hand-holding-usd me-3", style={"fontSize": "23px"}),
# html.Span("Venta Semanal",
#         className=" mycard-header")
# ]),
# ),

#######################################
# Layout
#######################################


def inicio_layout():
    layout = html.Div([
        html.Div([html.H2("Dashboard Principal"),
                  html.Img(src="..\\assets\\img\\analytics.png")
                  ], className="banner"),
        dbc.Row([

        ]),
        dbc.Row([
            dbc.Col(card_sales),
            dbc.Col(card_new_client),
            dbc.Col(card_cirugias),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([html.B("Seleccione Clinica"),
                            dcc.Dropdown(
                                id="clinic-select",
                                options=[{"label": i, "value": i} for i in clinic_list],
                                value=clinic_list[0],
                            ),]),
                    dbc.Col([html.B("Seleccione Rango Fechas    "),
                             html.I(className="fa-solid fa-calendar",
                       style={"fontSize": "20px", "align-self": "flex-end"}),
                            dcc.DatePickerRange(
                                id="date-picker-select",
                                start_date=dt(2014, 1, 5),
                                end_date=dt(2014, 1, 12),
                                min_date_allowed=dt(2014, 1, 1),
                                max_date_allowed=dt(2014, 12, 31),
                                initial_visible_month=dt(2014, 1, 1),
                                calendar_orientation='horizontal',
                                style={'width': '90%'}
                ),]),
                    ]),
                dbc.Row([html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Volumen Pacientes"),
                        html.Hr(),
                        dcc.Graph(id="patient_volume_hm"),
                    ],
                ),])
            ], width=6),
            dbc.Col([html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),                     
                     html.Br(),                     
                     html.Br(),
                    html.Div([
                    #html.H1("Análisis de la Clínica Veterinaria"),
                    dcc.Graph(figure=fig_burbuja)
                    ])
            ], width=6)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dcc.Graph(
                        id='ventas-medicamentos-chart',
                        figure=fig_ventas_medicamentos
                    ),
                    style={"border-radius": "15px"}
                ),
            ], width=6),
            dbc.Col([
                html.Div(
                    dcc.Graph(
                        id='subscriptores-chart',
                        figure=fig_subscriptores
                    ),
                    className='divBorder'
                )
            ], width=6)
        ])



        #    dbc.Row([
        #         dbc.Col([
        #             dcc.Graph(id='ventas-medicamentos-chart',
        #                       figure=fig_ventas_medicamentos,
        #                       style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'},
        #                       ),
        #         ], width=6),
        #         dbc.Col([
        #             dcc.Graph(id='subscriptores-chart',
        #                       figure=fig_subscriptores,
        #                       style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'},
        #                       )
        #         ], width=6)
        #     ])
    ])
    return layout


#######################################
# Callbacks
#######################################
@my_app.callback(
    Output("patient_volume_hm", "figure"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("clinic-select", "value"),
        Input("patient_volume_hm", "clickData"),
    ],
)
def update_heatmap(start, end, clinic, hm_click):
    start = start + " 00:00:00"
    end = end + " 00:00:00"   

    # Return to original hm(no colored annotation) by resetting
    return generate_patient_volume_heatmap(
        start, end, clinic, hm_click
    )




