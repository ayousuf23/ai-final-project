import base64
import io
import pandas as pd
from dash import Dash, html, dcc, dash_table, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.Center([html.H1("Linear Regression Tool")], style={"marginTop": 20}),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.H2("What is this tool?", style={"marginLeft": 20}),
                html.P(
                    "A tool for visualizing linear regression.",
                    style={"fontSize": 15, "marginLeft": 40},
                ),
            ]
        ),
        html.Div(
            [
                html.H2("How to use?", style={"marginLeft": 20}),
                html.P(
                    "Start either by uploading a .csv file, or interacting with the graph!",
                    style={"fontSize": 15, "marginLeft": 40},
                ),
                html.Ul(
                    [
                        html.Li(
                            "Make sure that the table has appropriate column headers that can be extracted as features",
                            style={"marginLeft": 60},
                        ),
                        html.Li(
                            [
                                "Try and make sure that there is no missing data in the table, click ",
                                html.A(
                                    "here",
                                    href="https://www.analyticsvidhya.com/blog/2021/05/dealing-with-missing-values-in-python-a-complete-guide/",
                                    target="_blank",
                                ),
                                " for more information",
                            ],
                            style={"marginLeft": 60},
                        ),
                    ],
                    style={"fontSize": 15},
                ),
            ]
        ),
        html.Center(
            html.Div(
                [
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            ["Drag and Drop or ", html.A("Select Files")]
                        ),
                        style={
                            "width": "95%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "marginBottom": "2.5%",
                            "cursor": "pointer",
                        },
                        multiple=False,
                    ),
                    html.Div(id="output-data-upload"),
                ]
            )
        ),
        html.Hr(),
        html.Div(
            [
                dbc.Toast(
                    "Please upload a .csv or .xlsx file",
                    id="error-toast",
                    header="Invalid File Type",
                    is_open=False,
                    dismissable=True,
                    icon="danger",
                    duration=4000,
                )
            ],
            style={"position": "fixed", "top": "2rem", "right": "2rem"},
        ),
    ]
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    if "csv" in filename:
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    elif "xlsx" in filename:
        df = pd.read_excel(io.BytesIO(decoded))

    return df


@app.callback(
    Output("output-data-upload", "children"),
    Output("error-toast", "is_open"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def update_output(contents, filename):
    if contents:
        if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
            return no_update, True

        try:
            df = parse_contents(contents, filename)
            return (
                html.Div(
                    [
                        html.H5(
                            ["Uploaded File: " + filename],
                            style={"marginBottom": "2.5%"},
                        ),
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="table",
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    data=df.to_dict("records"),
                                    style_cell={"textAlign": "left"},
                                    style_header={
                                        "backgroundColor": "rgb(230, 230, 230)",
                                        "fontWeight": "bold",
                                    },
                                    style_data={
                                        "whiteSpace": "normal",
                                        "height": "auto",
                                    },
                                )
                            ],
                            style={
                                "overflowX": "auto",
                                "marginLeft": "5%",
                                "marginRight": "5%",
                            },
                        ),
                        html.Hr(),
                    ],
                    style={"marginTop": 20},
                ),
                False,
            )
        except Exception as e:
            return (
                html.Div(["There was an error processing the file: {}".format(e)]),
                False,
            )
    return no_update, no_update


if __name__ == "__main__":
    app.run_server(debug=True)
