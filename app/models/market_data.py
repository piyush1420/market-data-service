from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.sql import func
from app.core.database import Base

class RawMarketData(Base):
    __tablename__ = "raw_market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    provider = Column(String(50), nullable=False)
    raw_response = Column(Text)
    
    # Create indexes for better query performance
    __table_args__ = (
        Index('idx_symbol_timestamp', 'symbol', 'timestamp'),
    )

class ProcessedPrice(Base):
    __tablename__ = "processed_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    provider = Column(String(50), nullable=False)
    
    __table_args__ = (
        Index('idx_processed_symbol_timestamp', 'symbol', 'timestamp'),
    )

class MovingAverage(Base):
    __tablename__ = "moving_averages"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    ma_5 = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_ma_symbol_timestamp', 'symbol', 'timestamp'),
    )

class PollingJob(Base):
    __tablename__ = "polling_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(50), unique=True, nullable=False)
    symbols = Column(Text, nullable=False)  # JSON string
    interval = Column(Integer, nullable=False)
    provider = Column(String(50), nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())