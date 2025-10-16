# 🧙 HNG 13 — Stage 0 Task

A simple FastAPI project that returns your profile info and a random cat fact dynamically fetched from the Cat Facts API.

---

## 🚀 Endpoint

**GET** `/me`

### Example Response

```json
{
  "status": "success",
  "user": {
    "email": "matthewiganga@gmail.com",
    "name": "Matthew Gift Iganya",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-16T13:31:23.784Z",
  "fact": "A cat usually has about 12 whiskers on each side of its face."
}
```

## Technology Stack
- Programming Language: Python
- Framework: FastAPI
- Deployment: Hosted on vercel
- CORS Handling: Configured to allow all origins


## How to Run Locally
1. Clone the repository:
   ```bash
   git clone hhttps://github.com/iganya/hng13-task-0.git
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
