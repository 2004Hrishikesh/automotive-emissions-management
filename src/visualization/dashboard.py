"""
Interactive Dashboard for Automotive Data Science Analytics Process
Implements comprehensive visualization of data processing pipeline
"""

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class AutomotiveAnalyticsDashboard:
    """Interactive dashboard for automotive data science process"""
    
    def __init__(self, datasets, quality_reports, cleaning_reports=None):
        self.datasets = datasets
        self.quality_reports = quality_reports
        self.cleaning_reports = cleaning_reports or {}
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Setup the dashboard layout"""
        
        self.app.layout = html.Div([
            html.H1("Automotive Data Science Analytics Dashboard", 
                   style={'textAlign': 'center', 'marginBottom': 30}),
            
            html.Div([
                html.H2("Phase II: Data Processing and Quality Assessment"),
                html.P("Student: Hrishikesh M | Registration: 22BCE0422 | Professor: Kumar K"),
            ], style={'textAlign': 'center', 'marginBottom': 30}),
            
            # Dataset Selection
            html.Div([
                html.Label("Select Dataset:"),
                dcc.Dropdown(
                    id='dataset-dropdown',
                    options=[{'label': name.replace('_', ' ').title(), 'value': name} 
                            for name in self.datasets.keys()],
                    value=list(self.datasets.keys())[0],
                    style={'marginBottom': 20}
                )
            ]),
            
            # Dashboard tabs
            dcc.Tabs(id="dashboard-tabs", value='overview', children=[
                dcc.Tab(label='Data Overview', value='overview'),
                dcc.Tab(label='Quality Assessment', value='quality'),
                dcc.Tab(label='Data Distributions', value='distributions'),
                dcc.Tab(label='Cleaning Process', value='cleaning'),
                dcc.Tab(label='Process Flow', value='process')
            ]),
            
            # Content area
            html.Div(id='dashboard-content', style={'marginTop': 20})
        ])
    
    def create_overview_content(self, selected_dataset):
        """Create overview content for selected dataset"""
        
        df = self.datasets[selected_dataset]
        
        # Basic statistics
        stats_table = dash_table.DataTable(
            data=df.describe().reset_index().to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.describe().reset_index().columns],
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
        
        # Dataset info
        info_data = [
            {"Metric": "Total Rows", "Value": f"{df.shape[0]:,}"},
            {"Metric": "Total Columns", "Value": f"{df.shape[1]:,}"},
            {"Metric": "Missing Values", "Value": f"{df.isnull().sum().sum():,}"},
            {"Metric": "Duplicate Rows", "Value": f"{df.duplicated().sum():,}"},
            {"Metric": "Memory Usage", "Value": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"},
            {"Metric": "Numeric Columns", "Value": f"{len(df.select_dtypes(include=[np.number]).columns)}"},
            {"Metric": "Categorical Columns", "Value": f"{len(df.select_dtypes(include=['object']).columns)}"}
        ]
        
        info_table = dash_table.DataTable(
            data=info_data,
            columns=[{"name": "Metric", "id": "Metric"}, {"name": "Value", "id": "Value"}],
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
        
        return html.Div([
            html.H3(f"Dataset Overview: {selected_dataset.replace('_', ' ').title()}"),
            
            html.Div([
                html.Div([
                    html.H4("Dataset Information"),
                    info_table
                ], style={'width': '48%', 'display': 'inline-block'}),
                
                html.Div([
                    html.H4("Statistical Summary"),
                    stats_table
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ])
        ])
    
    def create_quality_content(self, selected_dataset):
        """Create quality assessment content"""
        
        if selected_dataset not in self.quality_reports:
            return html.Div([html.H3("Quality report not available")])
        
        quality_report = self.quality_reports[selected_dataset]
        
        # Quality score gauge
        quality_score = quality_report.get('quality_score', 0)
        
        gauge_fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = quality_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Data Quality Score"},
            delta = {'reference': 90},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        
        gauge_fig.update_layout(height=400)
        
        # Completeness by column
        completeness_data = quality_report['completeness']['completeness_by_column']
        completeness_df = pd.DataFrame(list(completeness_data.items()), 
                                     columns=['Column', 'Completeness'])
        
        completeness_fig = px.bar(completeness_df, x='Column', y='Completeness',
                                 title='Data Completeness by Column')
        completeness_fig.update_layout(xaxis_tickangle=-45)
        
        return html.Div([
            html.H3(f"Quality Assessment: {selected_dataset.replace('_', ' ').title()}"),
            
            html.Div([
                html.Div([
                    dcc.Graph(figure=gauge_fig)
                ], style={'width': '48%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(figure=completeness_fig)
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ])
        ])
    
    def create_distributions_content(self, selected_dataset):
        """Create data distributions content"""
        
        df = self.datasets[selected_dataset]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return html.Div([html.H3("No numeric columns available for distribution analysis")])
        
        # Create distribution plots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[f'{col} Distribution' for col in numeric_cols[:4]]
        )
        
        for i, col in enumerate(numeric_cols[:4]):
            row = (i // 2) + 1
            col_pos = (i % 2) + 1
            
            fig.add_trace(
                go.Histogram(x=df[col], name=col, showlegend=False),
                row=row, col=col_pos
            )
        
        fig.update_layout(height=600, title_text="Data Distributions")
        
        return html.Div([
            html.H3(f"Data Distributions: {selected_dataset.replace('_', ' ').title()}"),
            dcc.Graph(figure=fig)
        ])
    
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        
        @self.app.callback(
            Output('dashboard-content', 'children'),
            [Input('dashboard-tabs', 'value'),
             Input('dataset-dropdown', 'value')]
        )
        def update_content(active_tab, selected_dataset):
            if active_tab == 'overview':
                return self.create_overview_content(selected_dataset)
            elif active_tab == 'quality':
                return self.create_quality_content(selected_dataset)
            elif active_tab == 'distributions':
                return self.create_distributions_content(selected_dataset)
            elif active_tab == 'cleaning':
                return html.Div([html.H3("Cleaning process visualization coming soon...")])
            elif active_tab == 'process':
                return html.Div([html.H3("Process flow diagram coming soon...")])
            else:
                return html.Div([html.H3("Select a tab to view content")])
    
    def run_dashboard(self, debug=True, port=8050):
        """Run the dashboard"""
        print(f"Starting Automotive Analytics Dashboard...")
        print(f"Dashboard will be available at: http://localhost:{port}")
        self.app.run_server(debug=debug, port=port)

if __name__ == "__main__":
    # This would be used when running as standalone
    print("Dashboard module loaded successfully")