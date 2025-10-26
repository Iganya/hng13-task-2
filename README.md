# 🧙 HNG 13 — Stage 3 Task

## Country Currency & Exchange API

A RESTful API built with FastAPI for fetching, storing, and managing country data with currency and exchange rates.
---

## 🚀 Endpoints

- POST /countries/refresh: Refresh data from external APIs.
- GET /countries: List countries (filters: ?region=Africa, ?currency=NGN, ?sort=gdp_desc).
- GET /countries/{name}: Get single country.
- DELETE /countries/{name}: Delete country.
- GET /status: Get status.
- GET /countries/image: Get summary image.


## Technology Stack
- Programming Language: Python
- Framework: FastAPI
- Deployment: Hosted Railway
- Database: Mysql


## How to Run Locally
1. Clone the repository:
   ```bash
   git clone hhttps://github.com/iganya/hng13-task-2.git
   cd your-repo
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
5. Access the API at `http://127.0.0.1:8000/`
