# Market Data Service

A robust, production‑ready FastAPI microservice for fetching, processing, and serving financial market data. Designed with scalability, modularity, and observability in mind—ideal for integration into trading platforms, analytics dashboards, or research pipelines.

---

## 🚀 Overview

This project provides:

* **Real‑time price retrieval** via data provider (e.g., Yahoo Finance, Alpha Vantage, Finnhub).
* **Scheduled polling** of symbols at configurable intervals, persisting raw and processed data.
* **Event streaming** pipeline using Kafka for downstream consumers.
* **Moving average computation** and storage for trend analysis.
* **Redis** caching layer for low‑latency responses.
* **Docker & Compose** for one‑command local deployment.
* **Comprehensive tests** (pytest) and **health monitoring** endpoints.

Ideal for developers and data engineers building financial analytics or algorithmic trading systems.

---

## 📂 Repository Structure

```text
market-data-service/
├── app/                      # Application source code
│   ├── core/                 # Database & Kafka configuration
│   ├── models/               # SQLAlchemy ORM models
│   ├── services/             # Business logic (producers, consumers, cache)
│   ├── api/                  # FastAPI route handlers
│   └── main.py               # FastAPI instantiation & startup hooks
├── tests/                    # Unit & integration tests
├── Dockerfile                # Container definition for the API service
├── docker-compose.yml        # Orchestrates API, Postgres, Kafka, Zookeeper, Redis, Adminer
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
├── docs/                     # Architecture diagrams & design notes
└── README.md                 # Project documentation (this file)
```

---

## 🛠️ Prerequisites

* **Git** (>=2.30)
* **Python** (>=3.8)
* **Docker & Docker Compose** (for local containerized development)
* **Kafka** & **Zookeeper** (included via Compose)
* **PostgreSQL** & **Redis** (included via Compose)

---

## 💻 Installation & Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/piyush1420/market-data-service.git
   cd market-data-service
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

---

## 🐳 Running Locally with Docker Compose

1. **Start all services**

   ```bash
   docker-compose up -d
   ```

2. **Verify containers**

   ```bash
   docker-compose ps
   ```

3. **Access interactive API docs**
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

4. **Shutdown**

   ```bash
   docker-compose down
   ```

---

## 🎯 Configuration

All environment-specific settings (database URL, Kafka brokers, Redis URL) are managed via environment variables in `docker-compose.yml`. Refer to `app/core/config.py` for the full list.

---

## 🔧 Usage Examples

* **Health check**

  ```bash
  curl http://localhost:8000/health
  ```

* **Fetch latest price**

  ```bash
  curl "http://localhost:8000/prices/latest?symbol=AAPL&provider=yahoo_finance"
  ```

* **Schedule polling job**

  ```bash
  curl -X POST http://localhost:8000/prices/poll \
    -H "Content-Type: application/json" \
    -d '{"symbols":["AAPL","MSFT"],"interval":60,"provider":"yahoo_finance"}'
  ```

---

## 🧪 Testing

Run the full test suite with coverage reporting:

```bash
pytest --cov=app --cov-report=term-missing -v
```

---

## ⚙️ Continuous Integration & Deployment

A sample GitHub Actions workflow (`.github/workflows/ci.yml`) can:

1. **Lint** with `flake8`
2. **Test** with `pytest`
3. **Build** the Docker image
4. (Optional) **Publish** to Docker Hub or deploy to a staging environment

---

## 📈 Architecture

Detailed diagrams and design rationale live in the `docs/` directory. Highlights:

* **FastAPI** application layer
* **PostgreSQL** for durable storage
* **Kafka** event streaming
* **Redis** for high‑throughput caching
* **APScheduler** (or Celery) for scheduled polling

---

## 🚀 Future Enhancements

* Extract provider interface and implement Alpha Vantage and Finnhub providers
* Implement scheduler (APScheduler or Celery) to process `polling_jobs` automatically
* Enhance documentation with troubleshooting guides and advanced usage examples
* Expand test suite with integration and performance tests

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

Please adhere to the existing code style and add tests for new functionality.

---
