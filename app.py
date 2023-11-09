import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Read data from the first Excel file (your existing data)
df = pd.read_excel("wto-data.xlsx")

# Read data from the second Excel file (for the second chart)
df2 = pd.read_excel("wto-cumulative.xlsx")  # Replace with the actual path

# Read data from the third Excel file (for the third chart)
df3 = pd.read_excel("wto-relative-data.xlsx")  # Replace with the actual path

# Read data from the fourth Excel file (for the new chart)
df4 = pd.read_excel("wto-relative-data-cumulative.xlsx")  # Replace with the actual path

# Define unique options for Indicator, Importing Region, Exporter, and Commodity
indicator_options = ['Exports', 'Imports']  # Customize based on your data
region_options = ['World', 'Northern Africa', 'Eastern Africa']  # Customize based on your data
exporter_options = ['World', 'United States']  # Customize based on your data
commodity_options = ['Wheat']  # Only 'Wheat' as the option

# Extract year from the 'Date' column and create a 'Year' column for all dataframes
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')  # Convert 'Date' to datetime
df['Year'] = df['Date'].dt.year

df2['Date'] = pd.to_datetime(df2['Date'], format='%d/%m/%Y')  # Convert 'Date' to datetime
df2['Year'] = df2['Date'].dt.year

df3['Date'] = pd.to_datetime(df3['Date'], format='%d/%m/%Y')  # Convert 'Date' to datetime
df3['Year'] = df3['Date'].dt.year

df4['Date'] = pd.to_datetime(df4['Date'], format='%d/%m/%Y')  # Convert 'Date' to datetime
df4['Year'] = df4['Date'].dt.year

# Define hex codes for the lines and bars
line_colors = ['#638FA4', '#A4588F', '#8FA463']  # Hex codes for line and bar colors

# White theme for the entire app
app.layout = html.Div(style={'backgroundColor': 'white', 'color': 'black'}, children=[
    html.H1("Demo for Japanese project"),  # Updated title here
    html.Div([
        html.Label("Select Indicator:"),
        dcc.Dropdown(
            id='indicator-dropdown',
            options=[{'label': indicator, 'value': indicator} for indicator in indicator_options],
            value=indicator_options[0],  # Default selection ( first indicator)
            placeholder="Select Indicator",
            style={'backgroundColor': 'white', 'color': 'black'}  # Dropdown style
        ),
    ]),
    html.Div([
        html.Label("Select Importing Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in region_options],
            value=region_options[0],  # Default selection (first region)
            placeholder="Select Importing Region",
            style={'backgroundColor': 'white', 'color': 'black'}  # Dropdown style
        ),
    ]),
    html.Div([
        html.Label("Select Exporter:"),
        dcc.Dropdown(
            id='exporter-dropdown',
            options=[{'label': exporter, 'value': exporter} for exporter in exporter_options],
            value=exporter_options[0],  # Default selection (first exporter)
            placeholder="Select Exporter",
            style={'backgroundColor': 'white', 'color': 'black'}  # Dropdown style
        ),
    ]),
    html.Div([
        html.Label("Select Commodity:"),
        dcc.Dropdown(
            id='commodity-dropdown',
            options=[{'label': commodity, 'value': commodity} for commodity in commodity_options],
            value=commodity_options[0],  # Default selection (only 'Wheat' available)
            placeholder="Select Commodity",
            style={'backgroundColor': 'white', 'color': 'black'}  # Dropdown style
        ),
    ]),
    html.Div([
        dcc.Graph(id='bar-chart', config={'displayModeBar': False}),  # First bar chart
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='second-line-chart', config={'displayModeBar': False}),  # Second line chart
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='third-line-chart', config={'displayModeBar': False}),  # Third line chart
    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    html.Div([
        dcc.Graph(id='fourth-line-chart', config={'displayModeBar': False}),  # Fourth line chart (new chart)
    ], style={'width': '48%', 'display': 'inline-block'}),
])

# Define callback to update the first grouped bar chart (similar to your existing code)
@app.callback(
    Output('bar-chart', 'figure'),
    Input('indicator-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('exporter-dropdown', 'value'),
    Input('commodity-dropdown', 'value')  # Add the 'Commodity' input
)
def update_grouped_bar_chart(selected_indicator, selected_region, selected_exporter, selected_commodity):
    # Determine the title based on the selected indicator
    if selected_indicator == "Exports":
        chart_title = "Bi-weekly Exports"  # Set the title to "Bi-weekly Exports"
    else:
        chart_title = "Bi-weekly Imports"  # Set the title to "Bi-weekly Imports"

    filtered_df = df[
        (df['Indicator'] == selected_indicator) &
        (df['Importing Region'] == selected_region) &
        (df['Exporter'] == selected_exporter) &
        (df['Commodity'] == selected_commodity)  # Filter by Commodity
    ]

    # Filter data for the specified years and dates (you can customize this)
    filtered_df = filtered_df[filtered_df['Year'].isin([2023, 2022, 2021])]
    filtered_df = filtered_df[filtered_df['Date'].dt.strftime('%d/%m').isin(['15/07', '31/07', '15/08', '31/08'])]

    # Create a grouped bar chart
    fig = go.Figure()

    years = [2021, 2022, 2023]
    dates = ['15/07', '31/07', '15/08', '31/08']

    for idx, year in enumerate(years):
        data = []
        for date in dates:
            filtered_data = filtered_df[
                (filtered_df['Year'] == year) &
                (filtered_df['Date'].dt.strftime('%d/%m') == date)
            ]
            if not filtered_data.empty:
                data.append(filtered_data['Values'].iloc[0])
            else:
                data.append(0)
        fig.add_trace(go.Bar(
            x=dates,
            y=data,
            name=str(year),
            marker_color=line_colors[idx],  # Set bar color
            marker_line_color=line_colors[idx]  # Set marker border color
        ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(
            title='Date',
            showgrid=False,  # Remove gridlines
        ),
        yaxis=dict(
            title='Tonnes',
            showgrid=False,  # Remove gridlines
        ),
        title=chart_title,  # Use the determined chart title
        paper_bgcolor='white',  # Background color
        plot_bgcolor='white',  # Plot area background color
        font=dict(color='black'),  # Text color
    )

    return fig

# Define callback to update the second line chart (synced with the same inputs)
@app.callback(
    Output('second-line-chart', 'figure'),
    Input('indicator-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('exporter-dropdown', 'value'),
    Input('commodity-dropdown', 'value')  # Add the 'Commodity' input
)
def update_second_line_chart(selected_indicator, selected_region, selected_exporter, selected_commodity):
    # Determine the title based on the selected indicator
    if selected_indicator == "Exports":
        chart_title = "Bi-weekly Cumulative Exports"  # Set the title to "Bi-weekly Cumulative Exports"
    else:
        chart_title = "Bi-weekly Cumulative Imports"  # Set the title to "Bi-weekly Cumulative Imports"

    filtered_df2 = df2[
        (df2['Indicator'] == selected_indicator) &
        (df2['Importing Region'] == selected_region) &
        (df2['Exporter'] == selected_exporter) &
        (df2['Commodity'] == selected_commodity)  # Filter by Commodity
    ]

    # Create a line chart
    fig = go.Figure()

    years = [2021, 2022, 2023]
    dates = ['15/07', '31/07', '15/08', '31/08']

    for idx, year in enumerate(years):
        data = []
        for date in dates:
            filtered_data = filtered_df2[
                (filtered_df2['Year'] == year) &
                (filtered_df2['Date'].dt.strftime('%d/%m') == date)
            ]
            if not filtered_data.empty:
                data.append(filtered_data['Values'].iloc[0])
            else:
                data.append(0)
        fig.add_trace(go.Scatter(
            x=dates,
            y=data,
            mode='lines+markers',
            name=str(year),
            line=dict(color=line_colors[idx]),  # Set line color
            marker=dict(color=line_colors[idx], line=dict(color=line_colors[idx]))  # Set marker color and border color
        ))

    fig.update_layout(
        xaxis=dict(
            title='Date',
            showgrid=False,  # Remove gridlines
        ),
        yaxis=dict(
            title='Tonnes',
            showgrid=False,  # Remove gridlines
        ),
        title=chart_title,  # Use the determined chart title
        paper_bgcolor='white',  # Background color
        plot_bgcolor='white',  # Plot area background color
        font=dict(color='black'),  # Text color
    )

    return fig

# Define callback to update the third line chart (synced with the same inputs)
@app.callback(
    Output('third-line-chart', 'figure'),
    Input('indicator-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('exporter-dropdown', 'value'),
    Input('commodity-dropdown', 'value')  # Add the 'Commodity' input
)
def update_third_line_chart(selected_indicator, selected_region, selected_exporter, selected_commodity):
    # Determine the title based on the selected indicator
    if selected_indicator == "Exports":
        chart_title = "Bi-weekly Cumulative Exports Relative Changes"  # Set the title to "Bi-weekly Cumulative Exports Relative Changes"
    else:
        chart_title = "Bi-weekly Cumulative Imports Relative Changes"  # Set the title to "Bi-weekly Cumulative Imports Relative Changes"

    # Create a line chart for '2023/24 vs 2022/23' and '2023/24 vs 3 year ave'
    fig = go.Figure()

    years = [2021, 2022, 2023]
    dates = ['15/07', '31/07', '15/08', '31/08']

    data_1 = df3[(df3['Indicator'] == selected_indicator) &
                 (df3['Importing Region'] == selected_region) &
                 (df3['Exporter'] == selected_exporter) &
                 (df3['Commodity'] == selected_commodity)]['2023/24 vs 2022/23']

    data_2 = df3[(df3['Indicator'] == selected_indicator) &
                 (df3['Importing Region'] == selected_region) &
                 (df3['Exporter'] == selected_exporter) &
                 (df3['Commodity'] == selected_commodity)]['2023/24 vs 3 year ave']

    for idx, data in enumerate([data_1, data_2]):
        fig.add_trace(go.Scatter(
            x=dates,
            y=data,
            mode='lines+markers',
            name=['2023/24 vs 2022/23', '2023/24 vs 3 year ave'][idx],
            line=dict(color=line_colors[idx]),  # Set line color
            marker=dict(color=line_colors[idx], line=dict(color=line_colors[idx]))  # Set marker color and border color
        ))

    fig.update_layout(
        xaxis=dict(
            title='Date',
            showgrid=False,  # Remove gridlines
        ),
        yaxis=dict(
            title='% ratio',
            showgrid=False,  # Remove gridlines
        ),
        title=chart_title,  # Use the determined chart title
        paper_bgcolor='white',  # Background color
        plot_bgcolor='white',  # Plot area background color
        font=dict(color='black'),  # Text color
    )

    return fig

# Define callback to update the fourth line chart (synced with the same inputs)
@app.callback(
    Output('fourth-line-chart', 'figure'),
    Input('indicator-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('exporter-dropdown', 'value'),
    Input('commodity-dropdown', 'value')  # Add the 'Commodity' input
)
def update_fourth_line_chart(selected_indicator, selected_region, selected_exporter, selected_commodity):
    # Determine the title based on the selected indicator
    if selected_indicator == "Exports":
        chart_title = "Bi-weekly Exports Relative Changes"  # Set the title to "Bi-weekly Exports Relative Changes"
    else:
        chart_title = "Bi-weekly Imports Relative Changes"  # Set the title to "Bi-weekly Imports Relative Changes"

    # Create a line chart for '2023/24 vs 2022/23' and '2023/24 vs 3 year ave' from df4
    fig = go.Figure()

    years = [2021, 2022, 2023]
    dates = ['15/07', '31/07', '15/08', '31/08']

    data_1 = df4[(df4['Indicator'] == selected_indicator) &
                 (df4['Importing Region'] == selected_region) &
                 (df4['Exporter'] == selected_exporter) &
                 (df4['Commodity'] == selected_commodity)]['2023/24 vs 2022/23']

    data_2 = df4[(df4['Indicator'] == selected_indicator) &
                 (df4['Importing Region'] == selected_region) &
                 (df4['Exporter'] == selected_exporter) &
                 (df4['Commodity'] == selected_commodity)]['2023/24 vs 3 year ave']

    for idx, data in enumerate([data_1, data_2]):
        fig.add_trace(go.Scatter(
            x=dates,
            y=data,
            mode='lines+markers',
            name=['2023/24 vs 2022/23', '2023/24 vs 3 year ave'][idx],
            line=dict(color=line_colors[idx]),  # Set line color
            marker=dict(color=line_colors[idx], line=dict(color=line_colors[idx]))  # Set marker color and border color
        ))

    fig.update_layout(
        xaxis=dict(
            title='Date',
            showgrid=False,  # Remove gridlines
        ),
        yaxis=dict(
            title='% ratio',
            showgrid=False,  # Remove gridlines
        ),
        title=chart_title,  # Use the determined chart title
        paper_bgcolor='white',  # Background color
        plot_bgcolor='white',  # Plot area background color
        font=dict(color='black'),  # Text color
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
