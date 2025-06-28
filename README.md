# Market Data Service

A FastAPI-based microservice for fetching and processing market data.

## Day 1 Progress ✅

- ✅ Basic FastAPI setup
- ✅ Two main endpoints: `/prices/latest` and `/prices/poll`
- ✅ Interactive API documentation
- ✅ Health check endpoint

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd market-data-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


Running the Service
bashuvicorn app.main:app --reload --host 0.0.0.0 --port 8000
API Endpoints
Get Latest Price
bashGET /prices/latest?symbol=AAPL&provider=yahoo_finance
Start Polling
bashPOST /prices/poll
Content-Type: application/json

{
  "symbols": ["AAPL", "MSFT"],
  "interval": 60,
  "provider": "yahoo_finance"
}
Testing

Interactive docs: http://localhost:8000/docs
Health check: http://localhost:8000/health

## Future Improvements
- Move API endpoints from main.py to api/prices.py for better organization
- Extract Pydantic models to schemas/ directory
- Implement provider interface for multiple data sources
