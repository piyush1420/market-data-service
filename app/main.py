from app.services.ma_consumer import ma_consumer
from app.services.cache_service import cache_service
from app.models.market_data import MovingAverage
from sqlalchemy import text

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import json
from sqlalchemy.orm import Session

from app.core.database import get_db, engine, Base
from app.services.market_data_service import MarketDataService
from app.models.market_data import PollingJob

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Market Data Service", version="1.0.0")

# Start moving average consumer
@app.on_event("startup")
async def startup_event():
    ma_consumer.start_consuming()
    print("Application started with Kafka consumer")

@app.on_event("shutdown")
async def shutdown_event():
    ma_consumer.stop_consuming()
    print("Application shutdown complete")
# Pydantic models
class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: str
    provider: str

class PollRequest(BaseModel):
    symbols: List[str]
    interval: int
    provider: str = "yahoo_finance"

class PollResponse(BaseModel):
    job_id: str
    status: str
    config: dict


@app.get("/prices/ma/{symbol}")
async def get_moving_average(symbol: str, db: Session = Depends(get_db)):
    """Get latest moving average for a symbol"""
    latest_ma = db.query(MovingAverage).filter(
        MovingAverage.symbol == symbol.upper()
    ).order_by(MovingAverage.timestamp.desc()).first()
    
    if not latest_ma:
        raise HTTPException(status_code=404, detail=f"No moving average found for symbol {symbol}")
    
    return {
        "symbol": latest_ma.symbol,
        "ma_5": latest_ma.ma_5,
        "timestamp": latest_ma.timestamp.isoformat() + "Z"
    }

@app.get("/cache/health")
async def cache_health():
    """Check Redis cache health"""
    is_healthy = cache_service.get_health()
    return {
        "cache": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.now().isoformat()
    }
@app.get("/")
async def root():
    return {"message": "Market Data Service is running with real data!"}

@app.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    provider: Optional[str] = Query("yahoo_finance", description="Data provider"),
    db: Session = Depends(get_db)
):
    """Get the latest price for a stock symbol from Yahoo Finance"""
    
    market_service = MarketDataService(db)
    
    # Try to get fresh data from Yahoo Finance
    price_data = market_service.get_latest_price(symbol, provider)
    
    if not price_data:
        # Fallback to cached data
        price_data = market_service.get_cached_price(symbol)
        if not price_data:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
    
    return PriceResponse(**price_data)

@app.post("/prices/poll", response_model=PollResponse)
async def start_polling(request: PollRequest, db: Session = Depends(get_db)):
    """Start polling for multiple stock symbols"""
    
    job_id = f"poll_{uuid.uuid4().hex[:8]}"
    
    # Store polling job in database
    polling_job = PollingJob(
        job_id=job_id,
        symbols=json.dumps(request.symbols),
        interval=request.interval,
        provider=request.provider,
        status="accepted"
    )
    db.add(polling_job)
    db.commit()
    
    return PollResponse(
        job_id=job_id,
        status="accepted",
        config={
            "symbols": request.symbols,
            "interval": request.interval,
            "provider": request.provider
        }
    )

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    cache_status = "healthy" if cache_service.get_health() else "unhealthy"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "cache": cache_status
    }

@app.get("/prices/history/{symbol}")
async def get_price_history(symbol: str, db: Session = Depends(get_db)):
    """Get recent price history for a symbol"""
    from app.models.market_data import ProcessedPrice
    
    prices = db.query(ProcessedPrice).filter(
        ProcessedPrice.symbol == symbol.upper()
    ).order_by(ProcessedPrice.timestamp.desc()).limit(10).all()
    
    if not prices:
        raise HTTPException(status_code=404, detail=f"No history found for symbol {symbol}")
    
    return {
        "symbol": symbol.upper(),
        "prices": [
            {
                "price": price.price,
                "timestamp": price.timestamp.isoformat() + "Z",
                "provider": price.provider
            }
            for price in prices
        ]
    }