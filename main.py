import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the dataset
try:
    dataset = pd.read_csv("projectk.csv")
except FileNotFoundError:
    raise FileNotFoundError("The file 'projectk.csv' was not found. Ensure it exists in the working directory.")

# Verify dataset structure
required_columns = ['Year', 'Sentiment', 'Retweets', 'Platform', 'Country', 'Day', 'Hour']
if not all(col in dataset.columns for col in required_columns):
    raise ValueError(f"Dataset must contain the following columns: {', '.join(required_columns)}")

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('SOCIAL MEDIA USAGE', style={'textAlign': 'center'}),

    # Input field for the year
    html.Div([
        html.Label("Enter Year:"),
        dcc.Input(id='year-input', type='number', placeholder='Enter year', debounce=True)
    ], style={'marginBottom': '20px', 'textAlign': 'center'}),

    # Graphs
    html.Div([
        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='hist-plot'),
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='bar-plot'),
    ], style={'marginTop': '20px'})
])

# Callback to update the graphs
@app.callback(
    [
        Output('scatter-plot', 'figure'),
        Output('hist-plot', 'figure'),
        Output('pie-chart', 'figure'),
        Output('bar-plot', 'figure')
    ],
    [Input('year-input', 'value')]
)
def update_plots(year):
    # Filter dataset by year
    filtered_data = dataset[dataset['Year'] == year] if year else dataset

    if filtered_data.empty:
        return (
            px.scatter(title="No data available for the selected year"),
            px.histogram(title="No data available for the selected year"),
            px.pie(title="No data available for the selected year"),
            px.bar(title="No data available for the selected year")
        )

    # Scatter plot
    unique_sentiments = filtered_data["Sentiment"].unique()
    scatter_plot = px.scatter(
        filtered_data,
        x="Retweets",
        y="Platform",
        title=f"Scatter Plot of Retweets vs Platform ({year})" if year else "Scatter Plot of Retweets vs Platform",
        color="Sentiment",
        color_discrete_sequence=px.colors.qualitative.Set1[:len(unique_sentiments)],
        labels={"Retweets": "Number of Retweets", "Platform": "Social Media Platform"},
        template="plotly_dark"
    )

    # Histogram
    hist_plot = px.histogram(
        filtered_data,
        x="Country",
        title=f"Histogram of Country ({year})" if year else "Histogram of Country",
        color_discrete_sequence=["blue"]
    )
    hist_plot.update_traces(marker=dict(line=dict(color="black", width=1)))

    # Pie chart
    pie_chart = px.pie(
        filtered_data,
        names='Day',
        values='Hour',
        title=f"Day-wise Usage ({year})" if year else "Day-wise Usage",
        template="plotly_dark"
    )

    # Bar plot
    bar_data = (

        filtered_data.groupby('Sentiment').size()
        .reset_index(name='Count')
        .sort_values('Count', ascending=False)
    )
    bar_plot = px.bar(
        bar_data,
        x='Sentiment',
        y='Count',
        title=f"Count of Sentiments ({year})" if year else "Count of Sentiments",
        color_discrete_sequence=["blue"]
    )

    return scatter_plot, hist_plot, pie_chart, bar_plot


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)