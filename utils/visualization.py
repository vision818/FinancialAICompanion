import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_portfolio_performance_chart(portfolio_data):
    """
    Create an interactive portfolio performance chart using plotly.
    Displays the portfolio value over time and the allocation breakdown.
    """
    # Assuming portfolio_data is a DataFrame with columns 'Date', 'Portfolio Value', and individual assets' values
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Portfolio Value', 'Asset Allocation'),
        row_heights=[0.7, 0.3]
    )

    # Portfolio value line chart
    fig.add_trace(
        go.Scatter(
            x=portfolio_data['Date'],
            y=portfolio_data['Portfolio Value'],
            mode='lines',
            name='Portfolio Value'
        ),
        row=1, col=1
    )

    # Asset allocation bar chart (Assumes portfolio_data includes columns for each asset)
    asset_columns = [col for col in portfolio_data.columns if col not in ['Date', 'Portfolio Value']]
    for asset in asset_columns:
        fig.add_trace(
            go.Bar(
                x=portfolio_data['Date'],
                y=portfolio_data[asset],
                name=asset
            ),
            row=2, col=1
        )

    # Update layout
    fig.update_layout(
        title='Portfolio Performance and Asset Allocation',
        yaxis_title='Value',
        yaxis2_title='Asset Allocation',
        xaxis_rangeslider_visible=False,
        height=800
    )

    return fig
