import streamlit as st
import os
os.environ["STREAMLIT_SERVER_PORT"] = "8501"

from utils.ai_helper import get_ai_response
from utils.API_integration import get_bitcoin_data, get_bitcoin_news
from utils.financial_data import get_portfolio_data
from utils.visualization import create_portfolio_performance_chart
from utils.database import init_db, get_db, ChatHistory, PortfolioAnalysis
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
    get_recommended_funds
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

# Streamlit page config
st.set_page_config(
    page_title="Portfolio Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
st.markdown("""
    <style>
        h1 { font-size: 28px !important; }
        .stApp { --st-page-icon-size: 30px !important; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_portfolio' not in st.session_state:
    st.session_state.current_portfolio = None

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("💰 Portfolio AI Advisor")
    st.markdown("---")

    # AI Chat in sidebar
    st.subheader("💬 Ask Portfolio AI")
    user_input = st.text_input("Ask anything about portfolio investing:")


    if st.button("Ask"):
        with st.spinner("Thinking..."):
            try:
                # Check if the user is asking about Bitcoin news
                if "bitcoin" in user_input.lower() and "news" in user_input.lower():
                    # Fetch Bitcoin news
                    bitcoin_news = get_bitcoin_news()
                    if bitcoin_news:
                        response = "\n".join(bitcoin_news)  # Join news items
                    else:
                        response = "Sorry, I couldn't fetch Bitcoin news at the moment."
                else:
                    # If not about Bitcoin news, call AI response function
                    response = get_ai_response(user_input)

                # Save chat to database
                with get_session() as db:
                    chat = ChatHistory(question=user_input, answer=response)
                    db.add(chat)
                    db.commit()

                # Update chat history
                st.session_state.chat_history.append({"question": user_input, "answer": response})
            except Exception as e:
                st.error(f"Error getting AI response: {str(e)}")

    # Display chat history from database
    with get_session() as db:
        chats = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(5).all()
        for chat in chats:
            st.markdown("---")
            st.markdown("**You:** " + chat.question)
            st.markdown("**AI:** " + chat.answer)

# Main content
st.title("Portfolio Manager")

# Tabs for different features
tab1, tab2 = st.tabs(["Portfolio Analysis", "Investment Planning"])

with tab1:
    st.header("📈 Portfolio Analysis")

    portfolio_type = st.selectbox("Select Portfolio Type", 
        ["Growth", "Income", "Balanced", "Tech-Focused", "Sustainable", "Custom"])

    if portfolio_type:
        try:
            # Fetch the portfolio data
            data = get_portfolio_data(portfolio_type)
            st.session_state.current_portfolio = data

            # Check if 'Date' exists, if not, create it from the index
            if 'Date' not in data.columns:
                data['Date'] = data.index  # or use another column if needed

            # Instead of checking for 'Open', we simply process the data without it
            # Save portfolio data to the database
            with get_session() as db:
                for index, row in data.iterrows():
                    analysis = PortfolioAnalysis(
                        portfolio_type=portfolio_type,
                        date=index.to_pydatetime(),
                        high_price=float(row.get('High', 0)),  # Default to 0 if 'High' is missing
                        low_price=float(row.get('Low', 0)),  # Default to 0 if 'Low' is missing
                        close_price=float(row.get('Close', 0)),  # Default to 0 if 'Close' is missing
                        volume=int(row.get('Volume', 0))  # Default to 0 if 'Volume' is missing
                    )
                    db.add(analysis)
                db.commit()

            st.success(f"Loaded data for {portfolio_type} Portfolio")
        except Exception as e:
            # Only log the error in the console, prevent user-facing errors
            print(f"Error loading portfolio data: {str(e)}")  # Log to console
            # Optionally, show a mild warning to the user
            st.warning("An issue occurred while loading the portfolio data.")


    if st.session_state.current_portfolio is not None:
        # Check if the 'Date' column exists before creating the chart
        if 'Date' not in st.session_state.current_portfolio.columns:
            st.error("Portfolio data does not contain a 'Date' column.")
        else:
            fig = create_portfolio_performance_chart(st.session_state.current_portfolio)
            st.plotly_chart(fig, use_container_width=True)

        # Display basic statistics
        st.subheader("Portfolio Performance Statistics")
        stats = st.session_state.current_portfolio.describe()
        st.dataframe(stats)
    else:
        st.info("Select a portfolio type to view analysis.")

with tab2:
    st.header("📊 Investment Planning")

    # Investment Key Details
    st.subheader("📌 Key Investment Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        initial_contribution = st.number_input("Initial Contribution ($)", min_value=1000, value=10000, step=500)
        median_market_outcome = st.text_input("Median Market Outcome", value="8%")
    with col2:
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=100, value=500, step=50)
        annual_total_return = st.text_input("Annual Total Return", value="12%")
    with col3:
        benchmark = st.text_input("Benchmark", value="S&P 500")
        max_drawdown = st.text_input("Max Drawdown", value="-15%")

    # Display Investment Summary
    st.markdown(
        f"""
        <div style="background-color:#FAF9F6; padding:10px; border-radius:10px; color:black; text-align:center;">
            <b>Initial Contribution:</b> ${initial_contribution} |
            <b>Monthly Contribution:</b> ${monthly_contribution} |
            <b>Median Market Outcome:</b> {median_market_outcome} |
            <b>Annual Total Return:</b> {annual_total_return} |
            <b>Benchmark:</b> {benchmark} |
            <b>Max Drawdown:</b> {max_drawdown}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

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
    timeline_data = create_investment_timeline_data(initial_contribution, investment_horizon)
    fig_timeline = create_investment_timeline(timeline_data)
    st.plotly_chart(fig_timeline, use_container_width=True)


# with tab2:
#     st.header("📊 Investment Planning")

#     # Investment Profile Input
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
#     with col2:
#         investment_horizon = st.slider("Investment Horizon (years)", 1, 30, 10)
#     with col3:
#         risk_tolerance = st.selectbox("Risk Tolerance", ["low", "medium", "high"])

#     # Get and display portfolio allocation
#     allocation = get_risk_profile(age, investment_horizon, risk_tolerance)
#     st.subheader("Suggested Portfolio Allocation")
#     fig_allocation = create_portfolio_allocation_chart(allocation)
#     st.plotly_chart(fig_allocation, use_container_width=True)

#     # Fund Recommendations
#     st.subheader("Recommended Funds")
#     recommended_funds = get_recommended_funds(risk_tolerance)
#     for fund in recommended_funds:
#         st.markdown(f"• {fund}")

#     # Display risk vs reward chart
#     st.subheader("Investment Options: Risk vs Reward")
#     risk_reward = get_investment_options()
#     fig_risk = create_risk_reward_chart(risk_reward)
#     st.plotly_chart(fig_risk, use_container_width=True)

#     # Investment Timeline
#     st.subheader("Investment Growth Timeline")
#     initial_investment = st.number_input("Initial Investment ($)", min_value=1000, value=10000)
#     timeline_data = create_investment_timeline_data(initial_investment, investment_horizon)
#     fig_timeline = create_investment_timeline(timeline_data)
#     st.plotly_chart(fig_timeline, use_container_width=True)

#     # Sustainable Investing
#     st.subheader("Sustainable Investment Options")
#     sustainable_portfolio = get_sustainable_investments()
#     fig_sustainable = create_portfolio_allocation_chart(sustainable_portfolio)
#     st.plotly_chart(fig_sustainable, use_container_width=True)

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

