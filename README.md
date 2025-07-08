# 🌍 Real Price Fetcher with Google Shopping

## 🚀 Features
- Scrapes real-time product prices from Google Shopping
- Supports localization using `country` (e.g., "US", "IN")
- Ready to deploy on Railway/Render (with Docker & Playwright)

## 🔧 Usage

### Run locally
```bash
pip install -r requirements.txt
playwright install
uvicorn api.index:app --reload
```

### Example cURL
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{ "country": "US", "query": "iPhone 16 Pro" }'
```

### Deploy to Railway
1. Go to https://railway.app/new
2. Select "Deploy from GitHub Repo"
3. Choose this project
4. Railway will auto-build using Dockerfile
