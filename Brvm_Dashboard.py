import dash
from dash import html, dcc, Input, Output, State, dash_table, no_update
import pandas as pd
import plotly.express as px
import pymongo
from bson.objectid import ObjectId
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from datetime import datetime



# Connection au serveur
client = pymongo.MongoClient(
    "mongodb+srv://lisa:ProjectData@cluster0.l1lw9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


# Ouverture de la base de données
db = client["brvm"]


# Collections
collection1 = db["brvm_obligations"]
collection2 = db["brvm_actions"]
collection3 = db["brvm_capitalisations"]
collection4 = db["brvm_indices"]
collection5 = db["brvm_market"]
collection6 = db["brvm_volumes"]


# Convertions des collections en dataframe panda
df1 = pd.DataFrame(list(collection1.find()))
# Avec pandas il est impossible d'effectuer des actions sur des colonnes si les noms de celles-ci contiennent des espaces.
df1.columns = [c.replace(' ', '_') for c in df1.columns] 
print(df1)

df2 = pd.DataFrame(list(collection2.find()))
df2.columns = [c.replace(' ', '_') for c in df2.columns]
print(df2)

df3 = pd.DataFrame(list(collection3.find()))
df3.columns = [c.replace(' ', '_') for c in df3.columns]
print(df3)

df4 = pd.DataFrame(list(collection4.find()))
df4.columns = [c.replace(' ', '_') for c in df4.columns]
print(df4)

df5 = pd.DataFrame(list(collection5.find()))
df5.columns = [c.replace(' ', '_') for c in df5.columns]
print(df5)

df6 = pd.DataFrame(list(collection6.find()))
df6.columns = [c.replace(' ', '_') for c in df6.columns]
print(df6)

# Date et Heure actuelle 
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Date & Heure = ", dt_string)

# Feuille de style, possible de changer voir les thèmes Bootstrap
external_stylesheets = [dbc.themes.LUMEN]

""" D'autres  thèmes sont disponibles  sur  https://bootswatch.com/3/ , 
il suffit de choisir un thème et de faire  external_stylesheets = [dbc.themes.CYBORG], le nom du thème en majuscule"""

#Définition de l'application, le meta_tags pour que le dashboard s'adapte pour tout type d'écrans
app = dash.Dash(__name__, suppress_callback_exceptions=True, title='BRVM Dashboard', external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])


# Variables supplémentaires crées, dictionnaires des secteurs et des entreprises qui y sont.
all_options = {category: list(df1[df1.Categorie == category]["Code_obligation"].unique()) for category in df1["Categorie"].unique()}
all_options2 = {category: list(df2[df2.Categorie == category]["Symbole"].unique()) for category in df2["Categorie"].unique()}
all_options3 = {category: list(df3[df3.Categorie == category]["Code_obligation"].unique()) for category in df3["Categorie"].unique()}
all_options4 = list(df4["Nom"].unique())
all_options5 = {category: list(df6[df6.Categorie == category]["Code_obligation"].unique()) for category in df6["Categorie"].unique()}



# Dictionnaire, Nom de l'entreprise: Abrégé nom de l'entreprise 
meta_data0 = {code: nom for (nom, code) in zip(list(df1["Nom"]), list(df1["Code_obligation"]))}
meta_data1 = {code: nom for (nom, code) in zip(list(df2["Nom"]), list(df2["Symbole"]))}
meta_data2 = {code: nom for (nom, code) in zip(list(df6["Nom"]), list(df6["Code_obligation"]))}


# Définition et style des différentes barres(Barres verticales et horizontales)
navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Barre Verticale", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        dbc.NavItem(dbc.NavLink("Obligations", href="/page-1")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Autres pages", header=True),
                dbc.DropdownMenuItem("Actions", href="/page-2"),
                dbc.DropdownMenuItem("Capitalisations", href="/page-3"),
                dbc.DropdownMenuItem("Indices", href="/page-4"),
                dbc.DropdownMenuItem("Marché et Volumes", href="/page-5"),
            ],
            nav=True,
            in_navbar=True,
            label="Plus",
        ),
    ],
    brand="Visualisation des données de la BRVM",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

# suite 
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# Style de la partie contenu(content) de la page  
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("", className="display-4"),
        html.Hr(),
        html.P(
            "", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Obligations", href="/page-1", id="page-1-link"),
                dbc.NavLink("Actions", href="/page-2", id="page-2-link"),
                dbc.NavLink("Capitalisations", href="/page-3", id="page-3-link"),
                dbc.NavLink("Indices", href="/page-4", id="page-4-link"),
                dbc.NavLink("Marché et Volumes", href="/page-5", id="page-5-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)



### Definition du layout(disposition des différents éléments)
## Page 1 
page_1 = html.Div([
    
    html.Hr(),
    
    dbc.Row(children=[html.Label("Catégorie"),]),

    dbc.Row([dbc.Col(html.Div(dcc.Dropdown(list(all_options.keys(), ),"Obligations d'Etat",id='category-radio', ),),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Dropdown(id='categorie_elmt-radio',),)),
                dbc.Col(html.Div(id='display-selected-values'),)
    ]),

    html.Hr(),
    html.Hr(),


    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-2',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-3',), ), width={'size':6,'order':2}),
    ]),
    dbc.Row([dbc.Col(html.Div(dcc.Graph(id='example-graph-4',), ), width={'size':6,'order':1}),
    ]),

    ])

## Page 2

page_2 = html.Div([
    html.Hr(),
    
    dbc.Row(children=[html.Label("Catégorie"),]),

    dbc.Row([dbc.Col(html.Div(dcc.Dropdown(list(all_options2.keys(), ),"Services publics",id='category-actions', ),),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Dropdown(id='categorie_elmt-actions',),), style={'display': 'inline-block'}),
                dbc.Col(html.Div(id='display-selected-values-actions'), style={'display': 'inline-block'})
    ]),

    html.Hr(),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-5',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-6',), ), width={'size':6,'order':2}),
    ]),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-7',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-8',), ), width={'size':6,'order':2}),
    ]),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-9',), ), width={'size':6,'order':1}),
        
    ]),
]
)

## Page 3
## Prétraitement des données
#Il faut changer le format des dates afin de pouvoir effectuer des actions sur elles, ex: les trier.
df3['Refresh_time'] = pd.to_datetime(df3['Refresh_time']) 
Refresh_time = df3.sort_values(by='Refresh_time')
# Récuperer la date la plus récentes  
recent_datetime = Refresh_time["Refresh_time"][(len(Refresh_time["Refresh_time"]))-1]
# Base contenant les données les plus récentes 
df3_prime = df3[df3.Refresh_time==recent_datetime]
fig11 = px.pie(df3_prime, values='Nombre_de_titres', names='Categorie', title='Volume des capitalisation par secteur')

page_3 = html.Div([
        html.Hr(),
        dbc.Row(children=[html.Label("Catégorie"),]),
        dbc.Row([dbc.Col(html.Div(dcc.Dropdown(list(all_options3.keys(), ),"Finances",id='category-capitalisations1', ),),style={'display': 'inline-block'}),
    ]),

    html.Hr(),
    html.Hr(),

        html.Div(dcc.Graph(id='graph-10',), ),

    html.Hr(),
    html.Hr(),

        html.Div(dcc.Graph(id='graph-11', figure = fig11), ),

    
    html.Hr(),
    dbc.Row(children=[html.Label("Catégorie"),]),

    dbc.Row([dbc.Col(html.Div(dcc.Dropdown(list(all_options3.keys(), ),"Finances",id='category-capitalisations2', ),),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Dropdown(id='categorie_elmt-capitalisations',),), style={'display': 'inline-block'}),
                dbc.Col(html.Div(id='display-selected-values-capitalisations'), style={'display': 'inline-block'})
    ]),
    
    html.Hr(),
    html.Hr(),
        html.Div(dcc.Graph(id='graph-11',), ),




])

## Page 4
page_4 = html.Div([
    html.Hr(),
    dbc.Row(children=[html.Label("Nom"),]),
    dbc.Row([dbc.Col(html.Div(dcc.Dropdown(all_options4, all_options4[0], id='category-indices', ),),style={'display': 'inline-block'}),
    ]),
    
    html.Hr(),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-12',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-13',), ), width={'size':6,'order':2}),
    ]),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-14',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-15',), ), width={'size':6,'order':2}),
    ]),
])

app.layout = html.Div(
    [
        dcc.Interval( #Actualisation de la de la page chaque 3 min
            id='interval-component',
            interval=1*1000*60*5, 
            n_intervals=0),
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)

## Page 5 

fig20 = px.area(df5, x='Date', y="Valeur_des_transactions" )
fig21 = px.area(df5, x='Date', y="Capitalisation_Actions" )
fig22 = px.area(df5, x='Date', y="Capitalisation_des_obligations" )
fig23 = px.area(df5, x='Date', y="Variation_veille_(%)_capitalisation_actions" )
fig24 = px.area(df5, x='Date', y="Variation_YTD_(%)_capitalisation_actions" )

fig20.update_layout(yaxis_title="Valeur des transactions", xaxis_title='Date')
fig21.update_layout(yaxis_title="Capitalisation Actions", xaxis_title='Date')
fig22.update_layout(yaxis_title="Capitalisation des obligations", xaxis_title='Date')
fig23.update_layout(yaxis_title="Variation veille (%) capitalisation actions", xaxis_title='Date')
fig24.update_layout(yaxis_title="Variation YTD (%) capitalisation actions", xaxis_title='Date')

fig20.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

fig21.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

fig22.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

fig23.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

fig24.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )



page_5 = html.Div([
    html.Hr(),
    
    dbc.Row(children=[html.Label("Catégorie"),]),

    dbc.Row([dbc.Col(html.Div(dcc.Dropdown(list(all_options5.keys(), ),"Finances",id='category-market-volumes', ),),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Dropdown(id='categorie_elmt-market-volumes',),), style={'display': 'inline-block'}),
                dbc.Col(html.Div(id='display-selected-values-market-volumes'), style={'display': 'inline-block'})
    ]),

    html.Hr(),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-16',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-17',), ), width={'size':6,'order':2}),
    ]),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-18',), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-19',), ), width={'size':6,'order':2}),
    ]),
    html.Hr(),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-20', figure = fig20), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-21', figure = fig21), ), width={'size':6,'order':2}),
        
    ]),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-22', figure = fig22), ), width={'size':6,'order':1}),
        dbc.Col(html.Div(dcc.Graph(id='example-graph-23', figure = fig23), ), width={'size':6,'order':2}),
        
    ]),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='example-graph-24', figure = fig24), ), width={'size':6,'order':1}),
    ]),
]
)



@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# Les callbacks
#  Les différentes pages 

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page_1
    elif pathname == "/page-2":
        return page_2
    elif pathname == "/page-3":
        return page_3
    elif pathname == "/page-4":
        return page_4
    elif pathname == "/page-5":
        return page_5
    # Si utilisateur essaies de rechercher des pages  différentes de celles-ci on lui retourne le msg 404
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# Boutons page 1
@app.callback(
    Output('categorie_elmt-radio', 'options'),
    Input('category-radio', 'value'))
def set_cat_elmt_options(selected_category):
    return [{'label': i, 'value': i} for i in all_options[selected_category]]


@app.callback(
    Output('categorie_elmt-radio', 'value'),
    Input('categorie_elmt-radio', 'options'))
def set_cat_elmt_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('category-radio', 'value'),
    Input('categorie_elmt-radio', 'value'))
def set_display_children(selected_cat, selected_cat_elmt):
    return u'{}:{}>>>{}'.format(
        selected_cat, selected_cat_elmt, meta_data0[selected_cat_elmt]
    )


# Boutons page 2
@app.callback(
    Output('categorie_elmt-actions', 'options'),
    Input('category-actions', 'value'))
def set_cat_elmt_options(selected_category):
    return [{'label': i, 'value': i} for i in all_options2[selected_category]]


@app.callback(
    Output('categorie_elmt-actions', 'value'),
    Input('categorie_elmt-actions', 'options'))
def set_cat_elmt_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('display-selected-values-actions', 'children'),
    Input('category-actions', 'value'),
    Input('categorie_elmt-actions', 'value'))
def set_display_children(selected_cat, selected_cat_elmt):
    return u'{}:{}>>>{}'.format(
        selected_cat, selected_cat_elmt, meta_data1[selected_cat_elmt]
    )

# Boutons page 3
@app.callback(
    Output('categorie_elmt-capitalisations', 'options'),
    Input('category-capitalisations2', 'value'))
def set_cat_elmt_options(selected_category):
    return [{'label': i, 'value': i} for i in all_options2[selected_category]]



@app.callback(
    Output('categorie_elmt-capitalisations', 'value'),
    Input('categorie_elmt-capitalisations', 'options'))
def set_cat_elmt_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('display-selected-values-capitalisations', 'children'),
    Input('category-capitalisations2', 'value'),
    Input('categorie_elmt-capitalisations', 'value'))
def set_display_children(selected_cat, selected_cat_elmt):
    return u'{}:{}>>>{}'.format(
        selected_cat, selected_cat_elmt, meta_data1[selected_cat_elmt]
    )

# Boutons page 5
@app.callback(
    Output('categorie_elmt-market-volumes', 'options'),
    Input('category-market-volumes', 'value'))
def set_cat_elmt_options(selected_category):
    return [{'label': i, 'value': i} for i in all_options2[selected_category]]


@app.callback(
    Output('categorie_elmt-market-volumes', 'value'),
    Input('categorie_elmt-market-volumes', 'options'))
def set_cat_elmt_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('display-selected-values-market-volumes', 'children'),
    Input('category-market-volumes', 'value'),
    Input('categorie_elmt-market-volumes', 'value'))
def set_display_children(selected_cat, selected_cat_elmt):
    return u'{}:{}>>>{}'.format(
        selected_cat, selected_cat_elmt, meta_data2[selected_cat_elmt])


# Graphs page 1
@app.callback(
    Output('example-graph-2', 'figure'),
    Output('example-graph-3', 'figure'),
    Output('example-graph-4', 'figure'),
    Input('categorie_elmt-radio', 'value'))
def update_figure(selected_category_elmt):
    filtered_df = df1[df1.Code_obligation == selected_category_elmt]

    filtered_df.columns = [c.replace('_', ' ') for c in filtered_df.columns]

    fig = px.area(filtered_df, x='Refresh time', y="Cours du jour en valeur")
    fig3 = px.area(filtered_df, x='Refresh time', y="Coupon couru")
    fig4 = px.area(filtered_df, x='Refresh time', y="Dernier paiement(valeur du coupon)")
    # fig.update_layout(transition_duration=500)

    fig.update_layout(yaxis_title='Cours du jour en valeur', xaxis_title='Date')
    fig3.update_layout(yaxis_title="Coupon couru", xaxis_title='Date')
    fig4.update_layout(yaxis_title="Dernier paiement(valeur du coupon)", xaxis_title='Date')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

    fig3.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig4.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    #fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    #fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig, fig3, fig4


# Graphs page 2
@app.callback(
    Output('example-graph-5', 'figure'),
    Output('example-graph-6', 'figure'),
    Output('example-graph-7', 'figure'),
    Output('example-graph-8', 'figure'),
    Output('example-graph-9', 'figure'),
    Input('categorie_elmt-actions', 'value'))
def update_figure(selected_category_elmt):
    filtered_df = df2[df2.Symbole == selected_category_elmt]

    filtered_df.columns = [c.replace('_', ' ') for c in filtered_df.columns]

    fig5 = px.area(filtered_df, x='Refresh time', y="Cours veille (FCFA)",)

    fig6 = px.area(filtered_df, x='Refresh time', y="Cours Ouverture (FCFA)")

    fig7 = px.area(filtered_df, x='Refresh time', y="Cours Clôture (FCFA)")

    fig8 = px.area(filtered_df, x='Refresh time', y="Volume")

    fig9 = px.area(filtered_df, x='Refresh time', y="Variation (%)",)

    
    
    # fig.update_layout(transition_duration=500)
    fig5.update_layout(yaxis_title="Cours veille (FCFA)", xaxis_title='Date')
    fig6.update_layout(yaxis_title="Cours Ouverture (FCFA)", xaxis_title='Date')
    fig7.update_layout(yaxis_title="Cours Clôture (FCFA)", xaxis_title='Date')
    fig8.update_layout(yaxis_title="Volume", xaxis_title='Date')
    fig9.update_layout(yaxis_title="Variation (%)", xaxis_title='Date')





    fig5.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

    fig6.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig7.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig8.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig9.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    #fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    #fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig5, fig6, fig7, fig8, fig9

# Graphs page3 
@app.callback(
    Output('graph-10', 'figure'),
    Input('category-capitalisations1', 'value'))
def update_figure(selected_category):
    df3_prime.columns = [c.replace('_', ' ') for c in df3_prime.columns]
    filtered_df = df3_prime[df3_prime.Categorie == selected_category]
    
    fig10 = px.treemap(filtered_df, path = ["Nom", "Cours du jour"] , values = "Capitalisation flottante" , color = 'Nombre de titres', color_continuous_scale='RdBu',)
    fig10.update_traces(root_color="lightgrey")

    fig10.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig10

@app.callback(
    Output('graph-11', 'figure'),
    Input('categorie_elmt-capitalisations', 'value'))
def update_figure(selected_category_elmt):
    filtered_df = df3[df3.Code_obligation == selected_category_elmt]

    filtered_df.columns = [c.replace('_', ' ') for c in filtered_df.columns]

    fig11 = px.area(filtered_df, x='Refresh time', y="Capitalisation globale",)

    fig11.update_layout(yaxis_title="Capitalisation globale", xaxis_title='Date')

    fig11.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
    ))
    return fig11

# Graphs page 4
@app.callback(
    Output('example-graph-12', 'figure'),
    Output('example-graph-13', 'figure'),
    Output('example-graph-14', 'figure'),
    Output('example-graph-15', 'figure'),
    Input('category-indices', 'value'))
def update_figure(selected_category_elmt):
    filtered_df = df4[df4.Nom == selected_category_elmt]

    filtered_df.columns = [c.replace('_', ' ') for c in filtered_df.columns]

    fig12 = px.area(filtered_df, x='Refresh time', y="Fermeture précédente",)

    fig13 = px.area(filtered_df, x='Refresh time', y="Fermeture")

    fig14 = px.area(filtered_df, x='Refresh time', y="Variation (%)")

    fig15 = px.area(filtered_df, x='Refresh time', y="Variation 31 décembre (%)")

    

    
    
    # fig.update_layout(transition_duration=500)
    fig12.update_layout(yaxis_title="Fermeture précédente", xaxis_title='Date')
    fig13.update_layout(yaxis_title="Fermeture", xaxis_title='Date')
    fig14.update_layout(yaxis_title="Variation (%)", xaxis_title='Date')
    fig15.update_layout(yaxis_title="Variation 31 décembre (%)", xaxis_title='Date')
    





    fig12.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

    fig13.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig14.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig15.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    
    #fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    #fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig12, fig13, fig14, fig15

# Graphs page 5 
@app.callback(
    Output('example-graph-16', 'figure'),
    Output('example-graph-17', 'figure'),
    Output('example-graph-18', 'figure'),
    Output('example-graph-19', 'figure'),
    Input('categorie_elmt-market-volumes', 'value'))
def update_figure(selected_category_elmt):
    filtered_df = df6[df6.Code_obligation == selected_category_elmt]

    filtered_df.columns = [c.replace('_', ' ') for c in filtered_df.columns]

    fig16 = px.area(filtered_df, x='Refresh time', y="Nombre de titres échangés",)

    fig17 = px.area(filtered_df, x='Refresh time', y="Valeur échangée")
   
    fig18 = px.area(filtered_df, x='Refresh time', y="PER")

    fig19 = px.area(filtered_df, x='Refresh time', y="Pourcentage de la valeur globale échangée")


    
    
    # fig.update_layout(transition_duration=500)
    fig16.update_layout(yaxis_title="Nombre de titres échangés", xaxis_title='Date')
    fig17.update_layout(yaxis_title="Valeur échangée", xaxis_title='Date')
    fig18.update_layout(yaxis_title="PER", xaxis_title='Date')
    fig19.update_layout(yaxis_title="Pourcentage de la valeur globale échangée", xaxis_title='Date')
   





    fig16.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )

    fig17.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig18.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    fig19.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])

        )
    )
    
    #fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    #fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig16, fig17, fig18, fig19

if __name__ == '__main__':
    app.run_server(debug=True)



