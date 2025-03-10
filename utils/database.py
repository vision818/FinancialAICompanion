from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class StockAnalysis(Base):
    __tablename__ = "stock_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    
    def to_dict(self):
        return {
            "date": self.date,
            "open": self.open_price,
            "high": self.high_price,
            "low": self.low_price,
            "close": self.close_price,
            "volume": self.volume
        }

class PortfolioAnalysis(Base):
    __tablename__ = "portfolio_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    portfolio_value = Column(Float, nullable=False)  # Total value of the portfolio
    risk_score = Column(Float)  # Risk score of the portfolio
    return_on_investment = Column(Float)  # ROI for the portfolio
    
    # Assuming a portfolio contains multiple stocks or assets
    # If you wish to track individual asset values, you could either
    # create separate columns for each asset or use a relationship 
    # with another table for asset breakdown
    asset_allocation = Column(Text)  # JSON or string representation of asset allocation

    def to_dict(self):
        return {
            "portfolio_type": self.portfolio_type,
            "date": self.date,
            "portfolio_value": self.portfolio_value,
            "risk_score": self.risk_score,
            "return_on_investment": self.return_on_investment,
            "asset_allocation": self.asset_allocation
        }

# Create database tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
