from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


def graph_app() -> Dash:
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    app = Dash(__name__)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })


    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"]
    )


    app.layout = html.Div(
        style={'backgroundColor': colors['background']}, 
        children=[
            html.H1(children="Hello Dash", 
                style={'textAlign': 'center', 'color': colors['text']}
            ),

            html.Div(children="""Dash Hello World""", 
                style={'textAlign': 'center','color': colors['text']}
            ),

            dcc.Graph(id="My Graph", figure=fig)
        ]
    )

    return app


def core_components() -> Dash:
    app = Dash(__name__)


    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

    df_fruit = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })


    fig = px.bar(df_fruit, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div([
        html.Div([
            dcc.Graph(id="My Graph", figure=fig),

            html.Br(),
            html.Label("Text Input"),
            dcc.Input(value="MTL", type="text"),

            html.Br(),
            html.Label('Slider'),
            dcc.Slider(
                min=0,
                max=9,
                marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 10)},
                value=5,
            ),
            
        ], style={'padding': 10, 'flex': 1}),


        html.Div([
            dcc.Graph(id='graph-with-slider'),

            dcc.Slider(
                df['year'].min(),
                df['year'].max(),
                step=None,
                value=df['year'].min(),
                marks={str(year): str(year) for year in df['year'].unique()},
                id='year-slider'
            ),

            html.Br(),
            html.Label("Radio Items"),
            dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal')
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'})


    @app.callback(
        Output("graph-with-slider", "figure"),
        Input("year-slider", "value"))
    def update_fig(selected_year: int):
        filtered_df = df[df["year"] == selected_year]
        
        fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

        fig.update_layout()
        
        return fig

    return app


if __name__ == "__main__":
    core_components().run_server(debug=True)