from dash import html, dcc
import pandas as pd
import geopandas as gpd
import os


GEODATA_PATH = 'data/maharashtra_districts.geojson'
CSV_PATH = 'data/data.csv'

# Check if data files exist before attempting to load
data_files_exist = os.path.exists(GEODATA_PATH) and os.path.exists(CSV_PATH)

if data_files_exist:
    try:
        district_geodata = gpd.read_file(GEODATA_PATH)
        district_geodata['district'] = district_geodata['district'].str.strip().str.title()
        df = pd.read_csv(CSV_PATH)
        df['district_name'] = df['district_name'].str.strip().str.title()
    except Exception as e:
        print(f"Error loading data: {e}. Using empty dataframes.")
        district_geodata = gpd.GeoDataFrame()
        df = pd.DataFrame({'Commodity': [], 'district_name': [], 'APMC':[], 'min_price': [], 'max_price': [], 'modal_price': [], 'arrivals_in_qtl': []})
else:
    print(f"Warning: Data files '{GEODATA_PATH}' or '{CSV_PATH}' not found. Using empty dataframes.")
    district_geodata = gpd.GeoDataFrame()
    df = pd.DataFrame({'Commodity': [], 'district_name': [], 'APMC':[], 'min_price': [], 'max_price': [], 'modal_price': [], 'arrivals_in_qtl': []})

numeric_cols = ['min_price', 'max_price', 'modal_price', 'arrivals_in_qtl']
available_commodities = sorted(df['Commodity'].dropna().unique())
if not available_commodities:
    available_commodities = ['Placeholder Commodity']
available_metrics = numeric_cols

navbar = html.Div([
    html.H2("MH APMC Market Analysis", style={
        'margin': '0',
        'padding': '0 20px',
        'lineHeight': '60px',
        'color': 'black',
        'fontFamily': 'Arial, sans-serif',
        'fontWeight': 'bold',
        'letterSpacing': '1px'
    }),
    dcc.Checklist(
        id='theme-toggle',
        className="theme-toggle",
        options=[{'label': 'Theme', 'value': 'dark'}],
        value=[],  # empty = light mode
        inputStyle={"margin-right": "10px"},
        style={'marginLeft': 'auto','marginRight':'70px', 'fontWeight': 'bold', 'color': '#333'}
    )
], style={
    'position': 'fixed',
    'top': '0',
    'left': '0',
    'width': '100%',
    'height': '70px',
    'background': 'linear-gradient(90deg, #007ACC, transparent)',
    'boxShadow': '0 6px 15px rgba(0,0,0,0.3)',
    'zIndex': '1000',
    'display': 'flex',
    'alignItems': 'center',
    'padding': '0 20px',
})


layout = html.Div([
    dcc.Store(id='theme-state', data={'class': 'light-theme'}),
    navbar,    
    html.Div([
        html.Div([
            html.Div([
                html.Iframe(id='map-display', style={
                    'width': '100%',
                    'height': '600px',
                    'border': '1px solid #DDD',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
                    'marginBottom': '30px',
                    'backgroundColor': 'white'
                }),
            ]),
            html.Div([
                html.H3("📊 APMC K-Means Cluster Scatter Plot", id='scatter-title', style={
                    'textAlign': 'center',
                    'color': '#007ACC',
                    'marginBottom': '15px'
                }),
                dcc.Graph(id='cluster-scatter-chart', config={'displayModeBar': False}, style={
                    'width': '100%',
                    'height': '600px',
                    'border': '1px solid #DDD',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
                    'padding': '10px'
                })
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '12px'}),
        ], id='content-area', style={'flexGrow': 3, 'minWidth': '70%'}),

        html.Div([
            html.H3("Selection Filters", id='filter-title', style={
                'textAlign': 'center',
                'color': '#007ACC',
                'marginBottom': '20px'
            }),
            html.Label('Select Commodity:', id='label-commodity', style={'fontWeight': 'bold', 'color': '#333'}),
            dcc.Dropdown(
                id='commodity-selector',
                options=[{'label': c, 'value': c} for c in available_commodities],
                value=available_commodities[0],
                clearable=False,
                style={'marginBottom': '20px', 'color': '#333'}
            ),
            html.Label('Select X-Axis Metric (Clustering):', id='label-x', style={'fontWeight': 'bold', 'color': '#333'}),
            dcc.Dropdown(
                id='metric-x-selector',
                options=[{'label': m.replace('_', ' ').title(), 'value': m} for m in available_metrics],
                value='modal_price',
                clearable=False,
                style={'marginBottom': '20px', 'color': '#333'}
            ),
            html.Label('Select Y-Axis Metric (Clustering):', id='label-y', style={'fontWeight': 'bold', 'color': '#333'}),
            dcc.Dropdown(
                id='metric-y-selector',
                options=[{'label': m.replace('_', ' ').title(), 'value': m} for m in available_metrics],
                value='arrivals_in_qtl',
                clearable=False,
                style={'marginBottom': '35px', 'color': '#333'}
            ),
        ], id='filter-panel', style={
            'flexGrow': 1,
            'minWidth': '25%',
            'maxWidth': '350px',
            'padding': '25px',
            'backgroundColor': '#F8F9FA',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'height': 'fit-content'
        })
    ], id='main-container', style={
        'display': 'flex', 
        'flexDirection': 'row', 
        'margin': '0 auto', 
        'maxWidth': '1600px',
        'gap': '30px',
        'padding': '0 20px',
        'marginTop':'100px'
    })
], id='app-container', style={
    'backgroundColor': '#EBEFF3',
    'minHeight': '100vh',
    'padding': '20px 0'
})
