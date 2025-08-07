# Invoice Validator & Currency Converter

## Features
- Validates invoice fields
- Converts currency to USD using ExchangeRate API
- Returns JSON and optional PDF report
- Async API for better performance

## Prerequisites
### ExchangeRate-API Key
- To fetch real-time currency conversion rates, you need to register for an account on ExchangeRate-API and obtain an API key and save that key inside .env

## Run locally
### create Virtual Environment
```bash
python -m venv env
source env/Scripts/activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run Application
```bash
uvicorn app.main:app --reload
```

## Docker create image and run container
```bash
docker build -t invoice-service .
docker run -d -p 8001:8001 --env-file .env invoice-service
```

## test
```bash
 python -m unittest tests.test_report_generator
 ```