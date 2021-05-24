import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from style import SIDEBAR_STYLE, CONTENT_STYLE
import re
from ast import literal_eval

df = pd.read_csv('concat_df.csv')
reco_df = pd.read_csv('reco_df.csv')
year_df = pd.read_csv('year_df.csv')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


# 전체 데이터테이블 조회
def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns]) ),
        html.Tbody([
            html.Tr([ html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                      ]) for i in range(min(len(dataframe), max_rows)) ]) ])

# 추천 시스템
def find_title(df, noun, top_n=10):
    # df['nouns'] = df['nouns'].apply(literal_eval)
    df['in_nouns_literal'] = df['nouns'].apply(lambda x: True if noun in x else False)
    df['in_nouns_literal'].value_counts()
    title_index = df[df['in_nouns_literal'] == True].index.values
    new_df = df.iloc[title_index][['categories', 'title', 'funding_amounts', 'likes']]

    new_df = new_df[(new_df['categories'] == new_df['categories'].value_counts().index[0])]

    C = new_df['funding_amounts'].mean()
    m = new_df['likes'].quantile(0.6)

    # return new_df, C, m

    def weighted_funding_average(record):
        v = record['likes']
        R = record['funding_amounts']
        return ((v / (v + m)) * R) + ((m / (v + m)) * C)

    new_df['weighted_funding'] = new_df.apply(weighted_funding_average, axis=1)
    # new_df['weighted_funding'] = new_df['weighted_funding'].apply(lambda x: round(x,2))
    return new_df.sort_values('weighted_funding', ascending=False)[:top_n]

# 사이드바
sidebar = html.Div([
    html.H2('OOOA', className='display-4'),
    html.Hr(),
    html.P('Number of students per education', className='lead'),
    dbc.Nav([
        dbc.NavLink('Home', href='/', active='exact'),
        dbc.NavLink('page1', href='/page-1', active='exact'),
        dbc.NavLink('page2', href='/page-2', active='exact'),
        dbc.NavLink('page3', href='/page-3', active='exact'),
        dbc.NavLink('Dataframe', href='/dataframe', active='exact'),
        dbc.NavLink('추천시스템', href='/system', active='exact')
    ],
    vertical=True,
    pills=True),
],
style=SIDEBAR_STYLE)

# 검색
search_bar = dbc.Row([
    dbc.Col(dbc.Input(type='search', placeholder='Search')),
    dbc.Col(dbc.Button('Search', color='primary',className='ml-2'), width='auto')],
    no_gutters=True,
    className='ml-auto flex-nowrap mt-3 mt-md-0',
    align='center')

# 네비게이션바
navbar = html.Div([
    dbc.Navbar([
       html.A(
           dbc.Row([
               dbc.Col(html.Img(src=PLOTLY_LOGO, height='30px')),
               dbc.Col(dbc.NavbarBrand('Navbar', className='ml-2')),
           ], align='center', no_gutters=True),
           href='https://plot.ly',
       ),
        dbc.NavbarToggler(id='navbar-toggler'),
        # dbc.Collapse(search_bar, id='navbar-collapse', navbar=True),
    ])
])

content = html.Div(id='page-content', children=[], style=CONTENT_STYLE)


category = year_df['categories'].unique()
feature = ['target_amounts', 'funding_amounts', 'percentages', 'n_supporters', 'likes']

multiple_input = \
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in category],
                value=category[0]),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label':i, 'value':i} for i in ['Linear','log']],
                value='Linear',
                labelStyle={'display':'inline-block'})
        ],
        style={'width':'48%', 'display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in feature],
                value=feature[0]),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'log']],
                value='Linear',
                labelStyle={'display': 'inline-block'})
        ],
        style={'width':'48%', 'float':'right', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(id='indicator-graphic'),
            dcc.Slider(id='year-slider',
               min=year_df['start_year'].min(),
               max=year_df['start_year'].max(),
               value=year_df['start_year'].min(),
               marks={str(year):str(year) for year in year_df['start_year'].unique()},
               step=None)
        ])
    ])

