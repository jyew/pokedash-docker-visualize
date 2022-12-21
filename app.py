import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
import dash_auth
import os
from PIL import Image
from dash import Dash
from dash.dependencies import Input, Output


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'admin'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

ROOT = 'pokemon_jpg/'
df = pd.read_csv('pokemon.csv')
df_p = df[['pokedex_number', 'name', 'attack', 'defense', 'speed', 'sp_attack', 'sp_defense', 'hp']]
Types = ['against_bug', 'against_dark', 'against_dragon', 'against_electric',
         'against_fairy', 'against_fight', 'against_fire', 'against_flying',
         'against_ghost', 'against_grass', 'against_ground', 'against_ice',
         'against_normal', 'against_poison', 'against_psychic', 'against_rock',
         'against_steel', 'against_water'
         ]
df_t = df[Types]
df_t = pd.concat([df['name'], df_t], axis=1)
# add picture

all_generation_options = {}
for _generation in df.generation.unique():
    temp = df[df.generation == _generation]
    all_generation_options['Generation '+ str(_generation)] = list(temp.name.unique())
    all_generation_options['Generation '+ str(_generation)].sort()

# Design the layout of the dash board
app.layout = html.Div([
    html.H1('Pokemon ability Plot', style={'text-align': 'center'}),

    html.Div(children=[
        dcc.RadioItems(
            id='generation-dropdown',
            options=[{'label': k, 'value': k} for k in all_generation_options.keys()],
            value='Generation 1',
            style={'width': '23%', 'display': 'inline-block'}
        ),
    ]),   
    html.Br(),
    dcc.Dropdown(id='names-dropdown', value='Abra',
                searchable=True, style={'width': '33%'}),

    html.Br(),
    html.Div(children=[dcc.Graph(id='Pokemon pic', style={'width': '33%', 'display': 'inline-block'}),
                       dcc.Graph(id='Radar Plot', figure={}, style={'width': '33%', 'display': 'inline-block'}),
                       dcc.Graph(id='Against Type', figure={}, style={'width': '33%', 'display': 'inline-block'})
                       ]),
    html.Hr(),
    html.H1('Pokemon Generation Analysis', style={'text-align': 'center'}),
    html.Div(children=[dcc.Graph(id='Count of Generation', style={'width': '50%', 'display': 'inline-block'},
                        ),
                       dcc.Graph(id='Type Heatmap', style={'width': '50%', 'display': 'inline-block'}),
                       ]),
    html.Br(),
    html.Div(children=[dcc.Graph(id='Base Total Distribution', style={'width': '50%', 'display': 'inline-block'}),
                       dcc.Graph(id='Median Attributes Heatmap', style={'width': '50%', 'display': 'inline-block'}),
                       ]),
    html.Br(),
    html.Div(children=[dcc.Graph(id='Capture Rate Distribution', figure={}, style={'width': '50%', 'display': 'inline-block'}),
                       dcc.Graph(id='Base Total vs Capture Rate', figure={}, style={'width': '50%', 'display': 'inline-block'})
                       ]),
    html.Br(),
    html.Br(),
    html.Br(),

])

@app.callback(
    dash.dependencies.Output('names-dropdown', 'options'),
    [dash.dependencies.Input('generation-dropdown', 'value')])
def set_generation_options(selected_generation):
    return [{'label': i, 'value': i} for i in all_generation_options[selected_generation]]

@app.callback(
    dash.dependencies.Output('names-dropdown', 'value'),
    [dash.dependencies.Input('names-dropdown', 'options')])
def set_names_value(available_options):
    return available_options[0]['value']

@app.callback(
    [
     Output(component_id='Pokemon pic', component_property='figure'),
     Output(component_id='Radar Plot', component_property='figure'),
     Output(component_id='Against Type', component_property='figure'),
     Output(component_id='Count of Generation', component_property='figure'),
     Output(component_id='Type Heatmap', component_property='figure'),
     Output(component_id='Base Total Distribution', component_property='figure'),
     Output(component_id='Median Attributes Heatmap', component_property='figure'),
     Output(component_id='Capture Rate Distribution', component_property='figure'),
     Output(component_id='Base Total vs Capture Rate', component_property='figure'),
     ],
    [Input(component_id='names-dropdown', component_property='value')]
)



def update_output(Pokemon):
    dff_p = df_p.copy()

    dff_p = dff_p[dff_p['name'] == Pokemon] # get the target pokemon info
    dff_index = int(dff_p['pokedex_number'].values) # get the index of pokemon info
    
    
    df_selected_pokemon = df[df['name'] == Pokemon].iloc[0] 
    selected_generation = df_selected_pokemon['generation']
    selected_type1 = df_selected_pokemon['type1']
    selected_type2 = df_selected_pokemon['type2']
    

    print('current pokemon: ', Pokemon)
 
    img_path = ROOT + str(dff_index) + '.jpg'

    if os.path.isfile(img_path):
        img = np.array(Image.open(img_path))
    else:
        img = np.array(Image.open(ROOT + 'image_not_found.jpg'))
    
    
    fig = px.imshow(img)
    fig.update_layout(coloraxis_showscale=False, title_x=0.5, title_y=1,
                    title_text="Generation {}, Type: {}".format(selected_generation, selected_type1.capitalize()),)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    tmp_r = pd.DataFrame(dict(
         r=dff_p.values[0][2:],
         theta=dff_p.columns[2:]))
    fig_r = px.line_polar(tmp_r, r='r', theta='theta', line_close=True)
    fig_r.update_traces(fill='toself')
    fig_r.update_layout(title_text="{}'s Base Total Breakdown".format(Pokemon), title_x=0.5, title_y=1,)

    dff_t = df_t.copy()
    dff_t = dff_t[dff_t['name'] == Pokemon]
    tmp_t = pd.DataFrame(dict(
         Against=dff_t.values[0][1:],
         Type=dff_t.columns[1:]))
    fig_t = px.bar_polar(tmp_t, r="Against", theta="Type",color="Against")
    fig_t.update_layout(title_text="{}'s Effectiveness against Other Types".format(Pokemon), title_x=0.5, title_y=1,)

    ############### generations ##################
    # count of generations
    df_generation = df.pivot_table(index=['generation', 'is_legendary'], 
                               values='name', aggfunc=len)
    df_generation = df_generation.reset_index()
    df_generation.columns = ['Generation', 'Is Legendary', 'Count of Pokemon']
    df_generation['Is Legendary'] = df_generation['Is Legendary'].astype(str)

    # dynamic border width
    fig_4_border_width = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    fig_4_border_color = ['white','white','white','white','white','white','white']
    
    fig_4_border_width[int(selected_generation) - 1] = 5
    fig_4_border_color[int(selected_generation) - 1] = 'gold'

    fig_4 = px.bar(df_generation, x="Generation", y="Count of Pokemon", 
                color="Is Legendary") #, color_discrete_sequence=barColor                
    fig_4.update_traces(#marker_color='rgb(158,202,225)', 
                marker_line_color=fig_4_border_color,
                marker_line_width=fig_4_border_width, opacity=0.8)
    fig_4.update_layout(title_text='Number of Pokemons by Generation', title_x=0.5)

    # type breakdown in each generation
    df_5 = df.pivot_table(index=['generation', 'type1'], 
                                values=['name', 'base_total'], 
                                aggfunc={'name':len, 'base_total': np.mean})
    df_5 = df_5.reset_index()
    df_5.columns = ['Generation', 'Primary Type', 'Avg Base Total', 'Count of Pokemon']
    fig_5 = px.treemap(df_5, path=[px.Constant('Pokemon world'), 'Generation', 'Primary Type'], 
                    values='Count of Pokemon',
                    color='Avg Base Total',
                    )
    fig_5.update_layout(title_text='Tree Map of Pokemon World by Generation', title_x=0.5)

    # base total distribution in each generation
    df_6 = df[['generation', 'base_total', 'is_legendary']]
    df_6.columns = ['Generation', 'Base Total', 'Is Legendary']
    fig_6 = px.box(df_6, x="Generation", y="Base Total", points="all",
                color="Is Legendary")
    fig_6.update_layout(title_text='Distribution of Base Total by Generation', title_x=0.5)
    
    # Median of Attributes by Type of Non-legendary Pokémon
    df_9 = df.rename(columns={'generation': 'Generation'}).groupby(
                ['Generation']).median()[["attack", "sp_attack", "defense", 
                "sp_defense", "hp", "speed"]]  #, "base_total"
    df_9 = df_9.rename(columns={'generation': 'Generation'})
    fig_9 = px.imshow(df_9, text_auto=True)
    fig_9.update_layout(title_text='Median attributes of Pokemons by Generation', title_x=0.5)

    # capture rate distribution in each generation
    df_7 = df[['generation', 'capture_rate', 'is_legendary']]
    df_7.columns = ['Generation', 'Capture Rate', 'Is Legendary']
    df_7['Generation'] = df_7['Generation'].astype(int)
    df_7 = df_7.sort_values(by='Capture Rate')
    # df_7['Capture Rate'] = df_7['Capture Rate'].replace({'30 (Meteorite)255 (Core)': 30})
    # df_7['Capture Rate'] = df_7['Capture Rate'].astype(int)
    fig_7 = px.box(df_7, x="Generation", y="Capture Rate", points="all",
                color="Is Legendary"
                )
    fig_7.update_layout(title_text='Distribution of Capture Rate by Generation', title_x=0.5)

    # capture rate vs base total in each generation
    df_8 = df[['generation', 'capture_rate', 'is_legendary', 'base_total', 'name']]
    df_8.columns = ['Generation', 'Capture Rate', 'Is Legendary', 'Base Total', 'Name']
    df_8['Generation'] = df_8['Generation'].astype(str)
    # df_8['Capture Rate'] = df_8['Capture Rate'].replace({'30 (Meteorite)255 (Core)': 30})
    # df_8['Capture Rate'] = df_8['Capture Rate'].astype(int)
    fig_8 = px.scatter(df_8, x="Capture Rate", y="Base Total", 
                    hover_data=['Name'], color='Generation', trendline="ols")
    fig_8.update_layout(title_text='Base Total vs Capture Rate', title_x=0.5)

    return fig, fig_r, fig_t, fig_4, fig_5, fig_6, fig_9, fig_7, fig_8

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port=8050)
