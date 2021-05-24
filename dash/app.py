import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from style import SIDEBAR_STYLE, CONTENT_STYLE
from layouts import navbar, sidebar, content, generate_table, search_bar, multiple_input
import matplotlib.pyplot as plt

#Instantiates the Dash app and identify the server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
df = pd.read_csv('concat_df.csv')
year_df = pd.read_csv('year_df.csv')
server = app.server


app.layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    sidebar,
    content
])

@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')])
def render_page_content(pathname):
    # 최초경로 출력
    if pathname =='/':
        return [
            dbc.Jumbotron([

            ])
        ]
    # 페이지1 출력
    elif pathname =='/page-1':
        return [
                html.H1('카테고리별 평균 목표금액',
                        style={'textAlign':'center'}),
                multiple_input,
        ]
    # 페이지2 출력
    elif pathname == '/page-2':
        return [
                html.H1('Grad School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                          figure=px.bar(year_df, barmode='group', x=df['start_year'].unique(),
                                        y=df['start_year'].value_counts()))

        ]
    # 페이지3 출력
    elif pathname == '/page-3':
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                          figure=px.bar(df, barmode='group', x='Years',
                                        y=['Girls High School', 'Boys High School']))
        ]
    # 페이지4 출력
    elif pathname == '/dataframe':
        return [
                html.Div([
                    dbc.Button('Download CSV', id='btn_csv', color='primary', style={'margin':'1rem'}),
                    dcc.Download(id='download-dataframe-csv'),
                dbc.Table(generate_table(df),
                          bordered=True,
                          dark=True,
                          hover=True,
                          responsive=True,
                          striped=True),
                ])
        ]
    # 에러메세지 출력
    return dbc.Jumbotron([
        html.H1('404:not found', className='text-danger'),
        html.Hr(),
        html.P(f'The pathname {pathname} was not recognised..')
    ])

@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('btn_csv', 'n_clicks'),
    prevent_initial_call=True)
def download(n_clicks):
    return dcc.send_data_frame(df.to_csv, 'mydf.csv')

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year-slider', 'value')) 
def update_figure(xaxis_column_name, yaxis_column_name,
                  xaxis_type, yaxis_type,
                  year_value):
    # 년도별 필터 적용
    dff = year_df[year_df['start_year'] == year_value]
    fig = px.bar(x=dff[dff['categories'] == xaxis_column_name]['start_month'], # x 값 = 시작월
                 y=dff[dff['categories'] == xaxis_column_name][yaxis_column_name]),
    fig.update_layout(transition_duration=500)

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig

if __name__ =='__main__':
    app.run_server()