import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import networkx as nx
import psutil
import plotly.graph_objects as go
import numpy as np
np = 5  # ❌ This would cause issues!

app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div([
    html.H1("AI-Powered Deadlock Detection System", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(id='deadlock-graph'),
        dcc.Interval(id='graph-update', interval=5000, n_intervals=0)
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='cpu-gauge'),
        dcc.Graph(id='memory-gauge'),
        dcc.Interval(id='cpu-memory-update', interval=2000, n_intervals=0)
    ], style={'width': '49%', 'display': 'inline-block'}),
])


# Function to generate the deadlock graph
def generate_deadlock_graph():
    G = nx.DiGraph()
    
    # Simulated process-resource dependencies
    edges = [(1, 'R1'), ('R1', 2), (2, 'R2'), ('R2', 3), (3, 'R3'), ('R3', 1)]  
    G.add_edges_from(edges)

    try:
        cycle = nx.find_cycle(G, orientation="original")
        deadlock_nodes = [node for edge in cycle for node in edge]
    except nx.NetworkXNoCycle:
        deadlock_nodes = []  # No deadlock detected

    pos = nx.spring_layout(G, seed=42)  # Fixed seed for consistent layout
    edge_x, edge_y = [], []

    # Draw edges
    for edge in G.edges():
        if edge[0] in pos and edge[1] in pos:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color="gray"),
        hoverinfo="none",
        mode="lines"
    )

    node_x, node_y, node_color = [], [], []

    for node in G.nodes():
        if node in pos:
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_color.append("red" if node in deadlock_nodes else "lightblue")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=[str(n) for n in G.nodes()],
        marker=dict(size=20, color=node_color),
        hoverinfo="text"
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        title="Deadlock Detection Graph",
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig


# Callback to update the deadlock graph
@app.callback(Output('deadlock-graph', 'figure'), Input('graph-update', 'n_intervals'))
def update_deadlock_graph(n_intervals):
    return generate_deadlock_graph()


# Callback to update CPU & Memory Gauges
@app.callback(
    [Output('cpu-gauge', 'figure'), Output('memory-gauge', 'figure')],
    Input('cpu-memory-update', 'n_intervals')
)
def update_cpu_memory_graph(n_intervals):
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    cpu_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cpu,
        title={"text": "CPU Usage (%)"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "blue"}}
    ))

    memory_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=memory,
        title={"text": "Memory Usage (%)"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "red"}}
    ))

    return cpu_fig, memory_fig


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)

