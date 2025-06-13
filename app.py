# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import dash_bootstrap_components as dbc

# Login
from flask_login import logout_user, current_user
from login import login, error, profile, user_admin

# file imports
from maindash import my_app
from components.inicio import inicio
from components.finanzas import finanzas
from components.analysis import analysis



#######################################
# Initial Settings
#######################################
server = my_app.server

CONTENT_STYLE = {
    # "transition": "margin-left .1s",
    # "padding": "2rem 2rem",
    'backgroundColor': '#D8DAE1',
}

########################################
sidebar = dbc.Nav(id='sideBar',
                  children=[],
                  vertical=True,
                  pills=True,
                  # className="sidebar",
                  )
my_app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Div([
            sidebar,
            html.Div(

                [
                    dash.page_container,
                ],
                className="content",
                # style=CONTENT_STYLE,
                id="page-content",
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
        ], style={'backgroundColor': '#D8DAE1'},
        ),
    ]
)


@my_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        if current_user.is_authenticated:
            return inicio.inicio_layout()
        else:
            return login.layout
    elif pathname == "/finanzas":
        if current_user.is_authenticated:
            return finanzas.finanzas_layout()
        else:
            return login.layout
    elif pathname == "/analysis":
        if current_user.is_authenticated:
            return analysis.analysis_layout()
        else:
            return login.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/inicio':
        if current_user.is_authenticated:
            return inicio.inicio_layout()
        else:
            return login.layout

    if pathname == '/profile':
        if current_user.is_authenticated:
            return profile.layout
        else:
            return login.layout

    if pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.admin == 1:
                return user_admin.layout
            else:
                return error.layout
        else:
            return login.layout

    return dbc.Container(
        children=[
            html.H1(
                "404 Error: Page Not found",
                style={"textAlign": "center", "color": "#082446"},
            ),
            html.Br(),
            html.P(
                f"Oh no! The pathname '{pathname}' was not recognised...",
                style={"textAlign": "center"},
            ),
            # image
            html.Div(
                style={"display": "flex", "justifyContent": "center"},
                children=[
                    html.Img(
                        src="https://elephant.art/wp-content/uploads/2020/02/gu_announcement_01-1.jpg",
                        alt="hokie",
                        style={"width": "400px"},
                    ),
                ],
            ),
        ]
    )


################################################################################
# ONLY SHOW NAVIGATION BAR WHEN A USER IS LOGGED IN
################################################################################
@my_app.callback(
    Output('sideBar', 'children'),
    [Input('page-content', 'children')])
def FnSideBar(input1):
    if current_user.is_authenticated:
        if current_user.admin == 1:
            navBarContents = [
                html.Div(
                    [
                        html.Div(
                            [
                                # html.H4("DEMO-VETE", style={"color": "white"}),
                                # style={"width": "50px", "height": "auto"}),
                                html.Img(src="..\\assets\\img\\logo.jpg", style={
                                         "width": "50px", "border-radius": "10px"}),
                            ],
                            className="sidebar-header",
                        ),
                        html.Br(),
                        html.Div(
                            style={"border-top": "2px solid white"}),
                        html.Br(),
                        # nav component
                        dbc.Nav(
                            [
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-home me-2"),
                                        html.Span("Inicio"),
                                    ],
                                    href="/",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-sack-dollar me-2"),
                                        html.Span("Finanzas"),
                                    ],
                                    href="/finanzas",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-chart-simple me-2"),
                                        html.Span(
                                            "Data Analysis"),
                                    ],
                                    href="/analysis",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-user me-2"),
                                        html.Span("Profile"),
                                    ],
                                    href="/profile",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-gear me-2"),
                                        html.Span("Admin"),
                                    ],
                                    href="/admin",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-right-from-bracket me-2"),
                                        html.Span("Logout"),
                                    ],
                                    href="/logout",
                                    active="exact",
                                ),
                            ],
                            # vertical=True,
                            # pills=True,
                        ),
                    ],
                    className="sidebar",
                )
            ]
            return navBarContents

        else:
            navBarContents = [
                html.Div(
                    [
                        html.Div(
                            [
                                # html.H4("DEMO-VETE", style={"color": "white"}),
                                # style={"width": "300px", "height": "auto"}
                                html.Img(src="..\\assets\\img\\logo.jpg", style={
                                         "width": "50px", "border-radius": "10px"}),
                            ],
                            className="sidebar-header",
                        ),
                        html.Br(),
                        html.Div(
                            style={"border-top": "2px solid white"}),
                        html.Br(),
                        # nav component
                        dbc.Nav(
                            [
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-home me-2"),
                                        html.Span("Inicio"),
                                    ],
                                    href="/",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-sack-dollar me-2"),
                                        html.Span("Finanzas"),
                                    ],
                                    href="/finanzas",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-chart-simple me-2"),
                                        html.Span(
                                            "Data Analysis"),
                                    ],
                                    href="/analysis",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-user me-2"),
                                        html.Span("Profile"),
                                    ],
                                    href="/profile",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fas fa-solid fa-right-from-bracket me-2"),
                                        html.Span("Logout"),
                                    ],
                                    href="/logout",
                                    active="exact",
                                ),
                            ],
                        ),
                    ],
                    className="sidebar",
                )
            ]
            return navBarContents

    else:
        return ''


if __name__ == "__main__":
    my_app.run_server(debug=False, host="127.0.0.8", port=8050)
