from dash import Dash, Input, Output, html, dcc, State
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.express as px

data=pd.read_csv('data/life_expectancy.csv')

app= Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
year_min=data['year'].min()
year_max=data['year'].max()

app.layout= html.Div([
    dbc.Col(
        [
            dbc.Row([
                dbc.Col(html.H1("Life Expectancy Dashboard", style={'color':'white', 'padding':'10px', 'margin':'10px'})),
                dbc.Col(html.A('Data Source',
                        href = 'https://www.worldometers.info/demographics/life-expectancy/',
                        target = '_blank',
                        style = {'color': 'black', 'margin':'10px', 'size':'15px'}), style={'textAlign':'right', 'marginTop':'60px'})                      
            ],style={'backgroundColor':'blue'}),
            dbc.Row([
                html.H3("Life expectancy by countries", style = {'textAlign':'center', 'color':'white', 'marginBottom':'20px', 'marginTop':'10px'}),
                dcc.RangeSlider(id= 'year-slider',
                                min= year_min,
                                max= year_max,
                                value= [year_min, year_max],
                                marks = {i: str(i) for i in range(year_min, year_max+1, 10)})                           
            ], style= {'backgroundColor':'darkblue'}),
            dbc.Row(
                dcc.Dropdown(id='countries-dropdown', options=data['country'].unique(), multi=True, style={'marginTop':'10px'})
            ),
            dbc.Row([
                html.Button('Submit', id='submit-button', style={'width':'80px', 'height':'35px', 'marginTop':'20px'}),
                dcc.Graph(id='graph')             
            ])
        ]
    )  
])

@app.callback(
    Output('graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('year-slider', 'value'),
    State('countries-dropdown', 'value')
)

def updateGraph(buttonclick, years_selected, countries_selected):
    if not countries_selected:
        return px.line(title="Please select at least one Country")
    else:
        filtered_data=data[data['country'].isin(countries_selected)]
    new_data=filtered_data[(filtered_data['year']>=years_selected[0]) & (filtered_data['year']<=years_selected[1])]
    fig=px.line(new_data, x='year', y="life expectancy", title='Life Expectancy', color="country")
    return fig

if __name__=='__main__':
    app.run(debug=True)