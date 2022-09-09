import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output 

import plotly.graph_objs as go

import numpy as np

class App:
    def __init__(self):

        selectVariable = [{'label': variable, 'value':variable} for variable in ['Opcion 1', 'Opcion 2']]

        self.app = dash.Dash(__name__)
        
        self.app.layout = html.Div(
            children = [
                # Header
                html.Div([
                    html.H1(children="IDEAM-GGLows Analytics",),
                    html.P(
                        children="Analyze the behavior of avocado prices"
                        " and the number of avocados sold in the US"
                        " between 2015 and 2018"),
                ]),
                # Nav
                html.Div([html.P("Nav")]),

                # Aside
                html.Div([html.P("Aside")]),

                # Body
                html.Div([
                    dcc.Dropdown(
                        id = 'selectVariable',
                        options = selectVariable,
                        value   = selectVariable[-1]['value'],
                    ),
                    dcc.Graph(id = 'tendentialGraph-1'),
                
                # Footer
                html.Div([html.P("Footer")]),
                ]),
            
            ]
        )

        @self.app.callback(Output('tendentialGraph-1', 'figure'),
                           [Input('selectVariable', 'value')])
        def updateTendentialGraph(selectVariable):
            if selectVariable == 'Opcion 1':
                fig = go.Figure(go.Scatter(x=np.random.rand(10),
                                           y=np.random.rand(10)))
            else:
                fig = go.Figure(go.Scatter(x=np.random.rand(100),
                                           y=np.random.rand(100)))

            return fig

    def __call__(self):
        self.app.run_server(debug=False)

# foo = App()
# print('Estoy en template')

