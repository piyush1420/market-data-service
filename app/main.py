from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="Market Data Service", version="1.0.0")

# Simple data models
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

# Fake data for testing (we'll replace this tomorrow with real data)
FAKE_PRICES = {
    "AAPL": 150.25,
    "MSFT": 380.50,
    "GOOGL": 140.75,
    "TSLA": 220.30
}

@app.get("/")
async def root():
    return {"message": "Market Data Service is running!"}

@app.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    provider: Optional[str] = Query("yahoo_finance", description="Data provider")
):
    """Get the latest price for a stock symbol"""
    
    symbol = symbol.upper()
    
    if symbol not in FAKE_PRICES:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    return PriceResponse(
        symbol=symbol,
        price=FAKE_PRICES[symbol],
        timestamp=datetime.now().isoformat() + "Z",
        provider=provider
    )

@app.post("/prices/poll", response_model=PollResponse)
async def start_polling(request: PollRequest):
    """Start polling for multiple stock symbols"""
    
    job_id = f"poll_{uuid.uuid4().hex[:8]}"
    
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
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}