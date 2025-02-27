import streamlit as st
import os
os.environ["STREAMLIT_SERVER_PORT"] = "8501"
from utils.ai_helper import get_ai_response
from utils.financial_data import get_stock_data
from utils.visualization import create_stock_chart
from utils.database import init_db, get_db, ChatHistory, StockAnalysis
from utils.portfolio_viz import (
    create_portfolio_allocation_chart,
    create_risk_reward_chart,
    create_investment_timeline
)
from utils.investment_advisor import (
    get_risk_profile,
    get_investment_options,
    create_investment_timeline_data,
    get_sustainable_investments,
    get_recommended_funds # Added function
)
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from contextlib import contextmanager

# Initialize database
init_db()

# Get database session
@contextmanager
def get_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

# Page configuration
st.set_page_config(
    page_title="Financial AI Assistant",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_stock' not in st.session_state:
    st.session_state.current_stock = None

# Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("💰 Financial Assistant")
    st.markdown("---")

    # Stock Analysis Section
    st.subheader("Stock Analysis")
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)")
    if stock_symbol:
        try:
            data = get_stock_data(stock_symbol)
            st.session_state.current_stock = data

            # Save stock data to database with proper type conversion
            with get_session() as db:
                for index, row in data.iterrows():
                    analysis = StockAnalysis(
                        symbol=stock_symbol,
                        date=index.to_pydatetime(),
                        open_price=float(row['Open']),
                        high_price=float(row['High']),
                        low_price=float(row['Low']),
                        close_price=float(row['Close']),
                        volume=int(row['Volume'])
                    )
                    db.add(analysis)
                db.commit()

            st.success(f"Loaded data for {stock_symbol}")
        except Exception as e:
            st.error(f"Error loading stock data: {str(e)}")

# Main content
st.title("Financial AI Assistant")

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["AI Chat", "Stock Analysis", "Investment Planning"])

with tab1:
    st.header("Ask me anything about finance!")

    # Chat interface
    user_input = st.text_input("Your question:", key="user_input")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            try:
                response = get_ai_response(user_input)

                # Save chat to database
                with get_session() as db:
                    chat = ChatHistory(
                        question=user_input,
                        answer=response
                    )
                    db.add(chat)
                    db.commit()

                st.session_state.chat_history.append({"question": user_input, "answer": response})
            except Exception as e:
                st.error(f"Error getting AI response: {str(e)}")

    # Display chat history from database
    with get_session() as db:
        chats = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(10).all()
        for chat in chats:
            st.markdown("---")
            st.markdown("**You:** " + chat.question)
            st.markdown("**AI:** " + chat.answer)

with tab2:
    st.header("Stock Analysis")

    if st.session_state.current_stock is not None:
        # Display stock chart
        fig = create_stock_chart(st.session_state.current_stock)
        st.plotly_chart(fig, use_container_width=True)

        # Display basic statistics
        st.subheader("Basic Statistics")
        stats = st.session_state.current_stock.describe()
        st.dataframe(stats)
    else:
        st.info("Enter a stock symbol in the sidebar to view analysis")

with tab3:
    st.header("Investment Planning")

    # Investment Profile Input
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
    with col2:
        investment_horizon = st.slider("Investment Horizon (years)", 1, 30, 10)
    with col3:
        risk_tolerance = st.selectbox("Risk Tolerance", ["low", "medium", "high"])

    # Get and display portfolio allocation
    allocation = get_risk_profile(age, investment_horizon, risk_tolerance)
    st.subheader("Suggested Portfolio Allocation")
    fig_allocation = create_portfolio_allocation_chart(allocation)
    st.plotly_chart(fig_allocation, use_container_width=True)

    # Fund Recommendations
    st.subheader("Recommended Funds")
    recommended_funds = get_recommended_funds(risk_tolerance)
    for fund in recommended_funds:
        st.markdown(f"• {fund}")

    # Display risk vs reward chart
    st.subheader("Investment Options: Risk vs Reward")
    risk_reward = get_investment_options()
    fig_risk = create_risk_reward_chart(risk_reward)
    st.plotly_chart(fig_risk, use_container_width=True)

    # Investment Timeline
    st.subheader("Investment Growth Timeline")
    initial_investment = st.number_input("Initial Investment ($)", min_value=1000, value=10000)
    timeline_data = create_investment_timeline_data(initial_investment, investment_horizon)
    fig_timeline = create_investment_timeline(timeline_data)
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Sustainable Investing
    st.subheader("Sustainable Investment Options")
    sustainable_portfolio = get_sustainable_investments()
    fig_sustainable = create_portfolio_allocation_chart(sustainable_portfolio)
    st.plotly_chart(fig_sustainable, use_container_width=True)

    # More detailed investment tips
    st.markdown("""
    ### Key Investment Tips:
    1. **Diversification** is key to reducing risk
       - Spread investments across different asset classes
       - Consider geographic diversification
       - Mix different investment styles

    2. **Start Early** to benefit from compound interest
       - Time in the market beats timing the market
       - Regular contributions add up significantly
       - Reinvest dividends and gains

    3. **Regular Rebalancing** keeps your portfolio aligned with your goals
       - Review portfolio quarterly
       - Adjust allocations as needed
       - Consider life changes and goals

    4. **Stay Informed** but avoid emotional decisions
       - Follow market trends
       - Research before investing
       - Don't panic during market volatility

    5. **Consider Costs** like fees and taxes
       - Compare expense ratios
       - Understand tax implications
       - Look for tax-efficient options
    """)