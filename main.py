from fastapi import FastAPI
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
import requests

app = FastAPI()


CAT_FACT_URL = "https://catfact.ninja/fact"


@app.get("/me")
def get_profile():
    """
    Returns profile information and a random cat fact.
    """
    try:
        response = requests.get(CAT_FACT_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        cat_fact = data.get("fact", "Cats are mysterious creatures!")
    except Exception:
        cat_fact = "Unable to fetch cat fact at the moment. Try again later."

    timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "user": {
                "email": "matthewiganga@gmail.com",
                "name": "Matthew Gift Iganya",
                "stack": "Python/FastAPI",
            },
            "timestamp": timestamp,
            "fact": cat_fact
        }
    )