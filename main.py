import streamlit as st
import os
from utils.ai_helper import get_ai_response
from utils.financial_data import get_stock_data
from utils.visualization import create_stock_chart
from utils.database import init_db, get_db, ChatHistory, StockAnalysis
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

            # Save stock data to database
            with get_session() as db:
                for index, row in data.iterrows():
                    analysis = StockAnalysis(
                        symbol=stock_symbol,
                        date=index,
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        volume=row['Volume']
                    )
                    db.add(analysis)
                db.commit()

            st.success(f"Loaded data for {stock_symbol}")
        except Exception as e:
            st.error(f"Error loading stock data: {str(e)}")

    # Export Options
    if st.session_state.current_stock is not None:
        if st.button("Export Data to CSV"):
            csv = st.session_state.current_stock.to_csv(index=True)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{stock_symbol}_data.csv",
                mime="text/csv"
            )

# Main content
st.title("Financial AI Assistant")

# Tabs for different features
tab1, tab2 = st.tabs(["AI Chat", "Stock Analysis"])

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