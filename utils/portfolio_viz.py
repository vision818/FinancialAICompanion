import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_portfolio_allocation_chart(allocations):
    """
    Create a pie chart showing portfolio allocation
    """
    df = pd.DataFrame({
        'Category': list(allocations.keys()),
        'Percentage': list(allocations.values())
    })

    fig = px.pie(
        df,
        values='Percentage',
        names='Category',
        title="Portfolio Allocation",
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
    df = pd.DataFrame([
        {'Option': k, 'Risk': v['risk'], 'Return': v['return']}
        for k, v in risk_levels.items()
    ])

    fig = px.scatter(
        df,
        x='Risk',
        y='Return',
        text='Option',
        title="Risk vs. Potential Return",
        labels={'Risk': 'Risk Level', 'Return': 'Potential Return (%)'}
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(size=15)
    )

    fig.update_layout(
        height=400,
        showlegend=False
    )

    return fig

def create_investment_timeline(goals):
    """
    Create a timeline visualization for investment goals
    """
    df = pd.DataFrame(goals)

    fig = px.line(
        df,
        x='year',
        y='amount',
        text='description',
        title='Investment Growth Timeline',
        labels={'year': 'Year', 'amount': 'Target Amount ($)'}
    )

    fig.update_traces(
        mode='lines+markers+text',
        textposition="top center",
        marker=dict(size=15)
    )

    fig.update_layout(
        height=400,
        showlegend=False
    )

    return fig