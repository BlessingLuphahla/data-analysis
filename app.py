from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)



def generate_histogram(df):
    plt.figure(figsize=(10, 4))
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for column in numeric_columns:
        df[column].hist()
        plt.title(f'Histogram of {column}')
        plt.tight_layout()
        break  # Only plot the first numeric column for simplicity
    return save_plot_to_base64()

def generate_pie_chart(df):
    plt.figure(figsize=(6, 6))
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        df[numeric_columns[0]].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title(f'Pie Chart of {numeric_columns[0]}')
    return save_plot_to_base64()

def generate_line_graph(df):
    plt.figure(figsize=(10, 4))
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        df[numeric_columns[0]].plot(kind='line')
        plt.title(f'Line Graph of {numeric_columns[0]}')
    return save_plot_to_base64()

def generate_sincos_plot(df):
    # Check if there are numeric columns in the DataFrame
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) == 0:
        return None  # No numeric data to plot

    # Use the first numeric column as the input for sin/cos/tan
    x = df[numeric_columns[0]].values

    # Generate the plot
    plt.figure(figsize=(10, 4))
    plt.plot(x, np.sin(x), label='sin(x)')
    plt.plot(x, np.cos(x), label='cos(x)')
    plt.plot(x, np.tan(x), label='tan(x)')
    plt.title(f'Sin, Cos, and Tan Plots for {numeric_columns[0]}')
    plt.legend()
    plt.tight_layout()

    return save_plot_to_base64()

def save_plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Load the data
        file = request.files['file']
        df = pd.read_csv(file)

        # Perform some basic analysis
        summary = df.describe().to_html()

        # Get the selected chart type
        chart_type = request.form.get('chart_type')

        # Generate the selected chart
        plot_data = None
        if chart_type == 'histogram':
            plot_data = generate_histogram(df)
        elif chart_type == 'pie':
            plot_data = generate_pie_chart(df)
        elif chart_type == 'line':
            plot_data = generate_line_graph(df)
        elif chart_type == 'sincos':
            plot_data = generate_sincos_plot(df)

        return render_template('index.html', summary=summary, plot_data=plot_data, chart_type=chart_type)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)