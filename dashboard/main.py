import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Carregue os dados de exemplo (substitua com seus próprios dados)
data = pd.read_csv('sample_data.csv')

# Crie um aplicativo Dash
app = dash.Dash(__name__)

# Defina o layout
app.layout = html.Div([
    # Cabeçalho
    html.H1('Dashboard de Finanças Pessoais'),
    
    # Campos de entrada para data e categoria
    html.Div([
        html.Label('Selecione o período de data:'),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=data['date'].min(),
            max_date_allowed=data['date'].max(),
            initial_visible_month=data['date'].max(),
            end_date=data['date'].max()
        ),
        html.Br(),
        html.Label('Selecione a categoria:'),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in data['category'].unique()],
            value='Todas'
        )
    ]),
    
    # Gráficos
    html.Div([
        # Gráfico de pizza para distribuição de categorias
        dcc.Graph(id='category-pie'),
        
        # Gráfico de linha para despesas mensais
        dcc.Graph(id='monthly-expenses'),
        
        # Gráfico de barras para comparação de categorias
        dcc.Graph(id='category-comparison')
    ]),
    
    # Painel de KPIs
    html.Div([
        html.H2('KPIs'),
        html.P(id='balance-kpi'),
        html.P(id='total-expenses-kpi'),
        html.P(id='total-income-kpi')
    ])
])

# Callbacks
@app.callback(
    Output('category-pie', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-dropdown', 'value')]
)
def update_category_pie(start_date, end_date, category):
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    if category != 'Todas':
        filtered_data = filtered_data[filtered_data['category'] == category]
    fig = px.pie(filtered_data, names='category', values='amount')
    return fig

@app.callback(
    Output('monthly-expenses', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_monthly_expenses(start_date, end_date):
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    fig = px.line(filtered_data, x='date', y='amount', color='category')
    return fig

@app.callback(
    Output('category-comparison', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_category_comparison(start_date, end_date):
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    fig = px.bar(filtered_data, x='category', y='amount')
    return fig

@app.callback(
    Output('balance-kpi', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_balance_kpi(start_date, end_date):
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    balance = filtered_data['amount'].sum()
    return f'Saldo: {balance:.2f}'

@app.callback(
    Output('total-expenses-kpi', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_total_expenses_kpi(start_date, end_date):
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    total_expenses = filtered_data[filtered_data['type'] == 'despesa']['amount'].sum()
    return f'Despesas totais: {total_expenses:.2f}'

@app.callback(
    Output('total-income-kpi', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_total_income_kpi(start_date, end_date):
    filtered_data = data[(data['date'] >= start_date