from dash import html, dcc, callback, Input, Output, State, exceptions, register_page
import pandas as pd
import base64
import io
import plotly.graph_objs as go
from linear_regression import gradient_descent_returns_weights_and_biases
import dash_bootstrap_components as dbc
import numpy as np

#  TODO: remove stuff in parentheses for toggle ON...after determining if file has header and displaying it

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1("Upload Your Own Dataset To Explore (2-variables)",
                        style={"font-size": "2rem"}),
                html.Div(
                    html.Span(
                        "Your csv should have two columns. The first one will be for the x-variable, and the second one is for the y-variable",
                        style={"font-size": "1rem"}
                    )
                ),
                html.Br(),
            ],
            style={"text-align": "center"},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Button(
                            className="button-container",
                            children=[
                                html.A(
                                    "Download Sample CSV",
                                    className="download-link",
                                    id="download-link",
                                    download="sample.csv",
                                    href="download_csv/",
                                ),
                                html.I(
                                    className="fas fa-download fa icon",
                                ),
                            ],
                        ),
                        html.Div("Upload .csv/.xslx file"),
                        dcc.Upload(
                            id="upload-data-component",
                            multiple=False,
                            children=html.Div(
                                [
                                    "Drag and Drop or ",
                                    html.A(
                                        "Select a File",
                                        style={"text-decoration": "underline"},
                                    ),
                                ],
                                className="upload-file-container",
                            ),
                        ),
                        html.Div(id="file-status-info"),
                        html.Br(),
                    ],
                    className="padded-container",
                ),

                html.Div(
                    children=[
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Add custom labels to axes (toggle ON if dataset doesn't have labels in header)",
                                    "value": "show_label_inputs",
                                }
                            ],
                            id="toggle_header_provided",
                            inline=True,
                            switch=True,
                        ),
                        html.Br(),
                    ],
                    className="padded-container",
                ),

                html.Div(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("x-axis label"),
                                            dbc.Input(
                                                id="x-axis-label",
                                                type="text",
                                                placeholder="X",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    width=6,
                                    style={"display": "inline-block"},
                                ),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("y-axis label"),
                                            dbc.Input(
                                                id="y-axis-label",
                                                type="text",
                                                placeholder="Y",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    width=6,
                                    style={"display": "inline-block"},
                                ),
                            ],
                            id="show_label_inputs",
                        ),
                    ],
                    style={
                        "padding-right": "25px",
                        "padding-left": "25px",
                    },
                ),



                html.Div(
                    children=[
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Specify initial weight and bias",
                                    "value": "show_init_w_b",
                                }
                            ],
                            id="toggle_init",
                            inline=True,
                            switch=True,
                        ),


                        html.Div(
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(
                                                        "Enter initial weight"
                                                    ),
                                                    dbc.Input(
                                                        id="init_w",
                                                        type="text",
                                                        placeholder="0",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(
                                                        "Enter initial bias"
                                                    ),
                                                    dbc.Input(
                                                        id="init_b",
                                                        type="text",
                                                        placeholder="0",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="padded-container",
                                ),
                            ],                     id="show_init_w_b",
                        ),
                        html.Br(),

                    ],

                    style={

                        "padding-right": "25px",
                        "padding-left": "25px",
                    }
                ),
                html.Div(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Learning Rate"),
                                dbc.Input(
                                    id="learning_rate",
                                    type="number",
                                    value=0.002,
                                    step=0.001,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Iteration Amount"),
                                dbc.Input(
                                    id="iteration_amount",
                                    type="number",
                                    value=100,
                                    min=1,
                                    max=500,
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                    className="padded-container",
                ),
            ],
        ),



        html.Div(
            className="padded-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="regression-graph",
                                config={"displayModeBar": True},
                                figure={
                                    "data": [
                                        {
                                            "x": 0,
                                            "y": 0,
                                            "type": "lines",
                                            "hovertemplate": " %{y:.2f}"
                                            "<extra></extra>",
                                        },
                                    ],
                                    "layout": {
                                        "title": {
                                            "text": "Relationship between X and Y",
                                            "x": 0.1,
                                            "xanchor": "left",
                                        },
                                        "xaxis": {"fixedrange": True},
                                        "yaxis": {
                                            "fixedrange": True,
                                        },
                                    },
                                },
                            ),
                            className="card",
                            width=12,
                        ),

                    ],
                ),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(children=[
                            html.Div(id='stats-container'),
                        ],
                            style={"padding-top": "2rem"}),
                        dbc.Col(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=dcc.Graph(
                                                id="cost-graph",
                                                config={
                                                    "displayModeBar": True},
                                                figure={
                                                    "data": [
                                                        {
                                                            "x": 0,
                                                            "y": 0,
                                                            "type": "lines",
                                                            "hovertemplate": " %{y:.2f}"
                                                            "<extra></extra>",
                                                        },
                                                    ],
                                                    "layout": {
                                                        "title": {
                                                            "text": "Cost over iterations",
                                                            "x": 0.5,
                                                            "xanchor": "center",
                                                        },
                                                        "xaxis": {"fixedrange": True},
                                                        "yaxis": {
                                                            "fixedrange": True,
                                                        },
                                                    },
                                                },
                                            ),                             className="card",
                                        ),
                                    ],
                                ),
                            ], align="top", class_name="cost-graph-container", style={"padding-top": "2rem"}
                        )
                    ],
                ),
            ],
        ),
    ]
)


@callback(
    Output('stats-container', 'children'),
    Input('upload-data-component', 'contents'),
    State('upload-data-component', 'filename'),
    State('upload-data-component', 'last_modified')
)
def update_stats_container(list_of_contents, list_of_names, list_of_dates):
    stats_html = dbc.Row(
        id='stats-container',
        children=[
            html.H4("Results"),
            html.Div("Equation of line", style={"font-weight": "bold"}),
            dbc.Row(
                children=[
                    dbc.Col(html.Div(id="equation")),
                    dbc.Col(dcc.Clipboard(
                        target_id="equation"), width=2, style={"color": "deepskyblue"})
                ],
                className="stats"
            ),
            html.Div("Weight", style={"font-weight": "bold"}),
            dbc.Row(
                children=[
                    dbc.Col(html.Div(id="weight")),
                    dbc.Col(dcc.Clipboard(
                        target_id="weight"), width=2, style={"color": "deepskyblue"})
                ],
                className="stats"
            ),
            html.Div("Bias", style={"font-weight": "bold"}),
            dbc.Row(
                children=[
                    dbc.Col(html.Div(id="bias")),
                    dbc.Col(dcc.Clipboard(
                        target_id="bias"), width=2, style={"color": "deepskyblue"})
                ],
                className="stats"
            ),
            html.Div("Final Cost", style={"font-weight": "bold"}),
            dbc.Row(
                children=[
                    dbc.Col(html.Div(id="cost")),
                    dbc.Col(dcc.Clipboard(
                        target_id="cost"), width=2, style={"color": "deepskyblue"})
                ],
                className="stats"
            ),
        ],
        align="top",
        className="flex-stats-container",
    )
    overlay = dbc.Row(

        children=[
            html.Div(
                children=[

                    html.H4("Results", style={
                        "opacity": 0}),
                    html.Div("Equation of line", style={
                        "font-weight": "bold", "opacity": 0}),
                    dbc.Row(
                        children=[
                            dbc.Col(html.Div(id="equation"),
                                    style={"opacity": 0}),
                            dbc.Col(dcc.Clipboard(target_id="equation"), width=2,
                                    style={"color": "deepskyblue", "opacity": 0})
                        ],
                        className="stats"
                    ),

                    html.Div("Weight", style={
                        "font-weight": "bold", "opacity": 0}),
                    dbc.Row(
                        children=[
                            dbc.Col(html.Div(id="weight"),
                                    style={"opacity": 0}),
                            dbc.Col(dcc.Clipboard(target_id="weight"), width=2,
                                    style={"color": "deepskyblue", "opacity": 0})
                        ],
                        className="stats"
                    ),
                    html.Div("Bias", style={
                        "font-weight": "bold", "opacity": 0}),
                    dbc.Row(
                        children=[
                            dbc.Col(html.Div(id="bias"),
                                    style={"opacity": 0}),
                            dbc.Col(dcc.Clipboard(target_id="bias"), width=2,
                                    style={"color": "deepskyblue", "opacity": 0})
                        ],
                        className="stats"
                    ),
                    html.Div("Final Cost", style={
                        "font-weight": "bold", "opacity": 0}),
                    dbc.Row(
                        children=[
                            dbc.Col(html.Div(id="cost"),
                                    style={"opacity": 0}),
                            dbc.Col(dcc.Clipboard(target_id="cost"), width=2,
                                    style={"color": "deepskyblue", "opacity": 0})
                        ],
                        className="stats"
                    ),

                    html.Div(
                        style={
                            "width": "100%",
                            "height": "100%",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "position": "absolute",
                            "top": "50%",
                            "left": "50%",
                            "transform": "translate(-50%, -50%)",
                            "backgroundColor": "#e5ecf6",
                            "padding": "1rem"
                        },
                        children=[
                            html.Div("Please upload a file to view results",
                                     className="stats-overlay")
                        ]
                    )
                ],
                style={"position": "relative"}
            )
        ],
        align="top",
        className="flex-stats-container",
    )

    return stats_html if list_of_contents is not None else overlay


@callback(
    [Output("show_label_inputs", "className"),
     Output("x-axis-label", "value"),
     Output("y-axis-label", "value")],
    [Input("toggle_header_provided", "value")],
    [State("x-axis-label", "value"),
     State("y-axis-label", "value")]
)
def show_label_name_inputs(toggle_value, x_axis_label, y_axis_label):
    if not toggle_value:
        exceptions.PreventUpdate()
    if toggle_value:
        return "padded-container", x_axis_label, y_axis_label
    else:
        return "hidden", "X", "Y"


@callback(
    [Output("show_init_w_b", "className"),
     Output("init_w", "value"),
     Output("init_b", "value")],
    [Input("toggle_init", "value")],
    [State("init_w", "value"),
     State("init_b", "value")]
)
def show_init_w_b(toggle_value, init_w, init_b):
    if toggle_value:
        return "padded-container", float(init_w), float(init_b)
    else:
        return "hidden", float(0), float(0)


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print(filename)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
            return df
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            return df
    except Exception as e:
        print("Error:", e)
        return None


@callback(Output('file-status-info', 'children'),
          Input('upload-data-component', 'contents'),
          State('upload-data-component', 'filename'),
          State('upload-data-component', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        dataframes = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
        print(dataframes)

        if not dataframes or dataframes[0] is None:
            return html.Div("Error. Please check that file type and/or format is valid.", style={'color': 'red'})
        df = dataframes[0]

        if df.shape[1] != 2:
            return html.Div("Invalid file format for 2D regression. Please upload a valid .csv or .xslx file (see sample.csv)", style={'color': 'red'})
        else:
            return html.Div(children=[
                html.Div("File uploaded successfully",
                         style={'color': 'green'}),
                html.Div(f"Filename: {list_of_names}")
            ])
    else:
        return html.Div("No data", style={'color': 'grey'})


@ callback(
    [Output("regression-graph", "figure"),
     Output("cost-graph", "figure"),
     Output('cost', 'children'),
     Output('weight', 'children'),
     Output('bias', 'children'),
     Output('equation', 'children')

     ],
    Input('upload-data-component', 'contents'),
    State('upload-data-component', 'filename'),
    State('upload-data-component', 'last_modified'),
    Input("x-axis-label", "value"),
    Input("y-axis-label", "value"),
    Input("learning_rate", "value"),
    Input("iteration_amount", "value"),
    Input("init_w", "value"),
    Input("init_b", "value"))
def update_chart(list_of_contents, list_of_names, list_of_dates, x_axis_label, y_axis_label, learning_rate, iteration_amount, init_w, init_b):
    regression_fig = go.Figure()
    cost_fig = go.Figure()

    regression_fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "Please upload a file to see linear regression visualization.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                        "size": 14
                }
            }
        ]
    )

    cost_fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "Please upload a file to see cost function.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                        "size": 14
                }
            }
        ]
    )

    children = []
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip([list_of_contents], [list_of_names], [list_of_dates])]

    if len(children) == 0:
        return [
            regression_fig,
            cost_fig,
            html.Div(children=0),
            html.Div(children=0),
            html.Div(children=0),
            html.Div(children=0)]
    elif len(children[0]) > 0 and children[0].shape[1] != 2:
        return [
            regression_fig,
            cost_fig,
            html.Div(children=0),
            html.Div(children=0),
            html.Div(children=0),
            html.Div(children=0)]
    else:
        df = children[0]
        init_b = float(init_b) if init_b else float(0)
        init_w = float(init_w) if init_w else float(0)
        learning_rate = float(learning_rate) if learning_rate else float(0.001)
        iteration_amount = int(
            iteration_amount) if iteration_amount else int(100)

        # TODO: determine if file contains header row!

        _, _, cost, w, b = gradient_descent_returns_weights_and_biases(
            df[0], df[1], init_w=init_w, init_b=init_b, alpha=learning_rate, iters=iteration_amount)

        x_axis_label = x_axis_label if x_axis_label else "X"
        y_axis_label = y_axis_label if y_axis_label else "Y"

        regression_fig = go.Figure()
        # trace for points
        regression_fig.add_trace(go.Scatter(
            x=df[0], y=df[1], mode='markers',  name="data",   hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"))

        # trace for regression line at any point on the line
        start = min(df[0])
        end = max(df[0])
        range_df = pd.DataFrame(np.arange(start, end, 0.01))
        regression_fig.add_trace(go.Scatter(
            x=range_df[0],
            y=w * range_df[0] + b,
            mode='lines',
            name='regression line',
            line=dict(color='red', dash='dash'),
            hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"
        ))

        regression_fig.update_layout(
            title={
                "text": f"{x_axis_label} vs {y_axis_label}",
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label,

        )

        cost_fig = go.Figure()
        cost_fig.update_layout(
            title={
                "text": "Cost vs. iterations",
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis={"fixedrange": True},
            yaxis={
                "fixedrange": True,
            },
            xaxis_title="Iterations",
            yaxis_title="Cost",

        )

        cost_fig.add_trace(go.Scatter(
            x=list(range(1, iteration_amount+1)), y=cost, mode='lines', name='Cost'))

        w_rounded = round(w, 3)
        b_rounded = round(b, 3)

        return [
            regression_fig,
            cost_fig,
            html.Div(children=cost[-1]),
            html.Div(children=w),
            html.Div(children=b),
            html.Div(children=[dcc.Markdown(
                f"y = **{w_rounded}**x + **{b_rounded}**")])
        ]
