import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_portfolio_allocation_chart(allocations):
    """
    Create a pie chart showing portfolio allocation
    """
    fig = px.pie(
        values=list(allocations.values()),
        names=list(allocations.keys()),
        title="Suggested Portfolio Allocation",
        hover_data=[f"{v:.1f}%" for v in list(allocations.values())],
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=False,
        height=400
    )
    return fig

def create_risk_reward_chart(risk_levels):
    """
    Create a scatter plot showing risk vs reward for different investment options
    """
    fig = go.Figure()
    
    # Add investment options
    for option, details in risk_levels.items():
        fig.add_trace(go.Scatter(
            x=[details['risk']],
            y=[details['return']],
            mode='markers+text',
            name=option,
            text=[option],
            textposition="top center",
            marker=dict(size=15),
        ))
    
    fig.update_layout(
        title="Risk vs. Potential Return",
        xaxis_title="Risk Level",
        yaxis_title="Potential Return (%)",
        height=400,
        showlegend=False
    )
    
    return fig

def create_investment_timeline(goals):
    """
    Create a timeline visualization for investment goals
    """
    fig = go.Figure()
    
    # Create timeline
    for goal in goals:
        fig.add_trace(go.Scatter(
            x=[goal['year']],
            y=[goal['amount']],
            mode='markers+text',
            name=goal['description'],
            text=[goal['description']],
            textposition="top center",
            marker=dict(size=15)
        ))
    
    fig.update_layout(
        title="Investment Timeline",
        xaxis_title="Year",
        yaxis_title="Target Amount ($)",
        height=400
    )
    
    return fig
