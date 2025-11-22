from dash import Dash, Input, Output, html, dcc, State
import pandas as pd
import plotly.express as px

app= Dash()
avocado= pd.read_csv('data/avocado.csv')
app.layout=html.Div([
    html.H1("Avocado Prices Dashboard"),
    html.P([dcc.Dropdown(id='cities-dropdown', options=avocado['geography'].unique(), value=avocado['geography'].unique()[0]), 
    dcc.Graph(id='graph')])
])

@app.callback(
    Output("graph", "figure"),
    Input("cities-dropdown", "value")
)

def update_graph(selected_city):
    filtered_avocado=avocado[avocado['geography']==selected_city]
    line_fig=px.line(filtered_avocado, x='date', y="average_price", title=f'Avocado Prices in {selected_city}', color="type")
    return line_fig
    

if __name__=="__main__":
    app.run(debug=True)