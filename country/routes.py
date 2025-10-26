import random
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
import os
from typing import List, Optional
from sqlalchemy import func, asc, desc
from datetime import datetime
from sqlalchemy.orm import Session
from db import get_db
from .models import Country
from .utils import generate_summary_image
from .schemas import CountryOut
import requests


router = APIRouter()


@router.post("/countries/refresh")
async def refresh_countries(db: Session = Depends(get_db)):
    try:
        try:
            countries_response = requests.get("https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies")
            countries_response.raise_for_status()
            countries_data = countries_response.json()
        except Exception:
            raise HTTPException(status_code=503, detail={"error": "External data source unavailable", "details": "Could not fetch data from Countries API"})

        try:
            rates_response = requests.get("https://open.er-api.com/v6/latest/USD")
            rates_response.raise_for_status()
            rates_data = rates_response.json()
            rates = rates_data["rates"]
        except Exception:
            raise HTTPException(status_code=503, detail={"error": "External data source unavailable", "details": "Could not fetch data from Exchange Rates API"})

        now = datetime.utcnow()
        for country_data in countries_data:
            if "name" not in country_data or "population" not in country_data:
                raise HTTPException(status_code=400, detail={"error": "Validation failed", "details": {"currency_code": "is required"}})

            name = country_data["name"]
            capital = country_data.get("capital")
            region = country_data.get("region")
            population = country_data["population"]
            flag_url = country_data.get("flag")
            currencies = country_data.get("currencies", [])

            currency_code = currencies[0]["code"] if currencies else None

            exchange_rate = None
            estimated_gdp = None
            if currency_code:
                exchange_rate = rates.get(currency_code)
                if exchange_rate:
                    random_mult = random.uniform(1000, 2000)
                    estimated_gdp = population * random_mult / exchange_rate
                else:
                    estimated_gdp = None  # Not found in rates
            else:
                estimated_gdp = 0  # No currencies

            # Find existing (case-insensitive)
            country_exist = db.query(Country).filter(func.lower(Country.name) == name.lower()).first()
            if country_exist:
                country_exist.capital = capital
                country_exist.region = region
                country_exist.population = population
                country_exist.currency_code = currency_code
                country_exist.exchange_rate = exchange_rate
                country_exist.estimated_gdp = estimated_gdp
                country_exist.flag_url = flag_url
                country_exist.last_refreshed_at = now
            else:
                new_country = Country(
                    name=name,
                    capital=capital,
                    region=region,
                    population=population,
                    currency_code=currency_code,
                    exchange_rate=exchange_rate,
                    estimated_gdp=estimated_gdp,
                    flag_url=flag_url,
                    last_refreshed_at=now
                )
                db.add(new_country)

        db.commit()

        # Generate summary image
        await generate_summary_image(db, now)

        return JSONResponse(content={"message": "Refresh successful"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})



@router.get("/countries", response_model=List[CountryOut])
async def get_countries(
    region: Optional[str] = Query(None),
    currency: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve list of countries with optional filtering and sorting."""
    try:
        query = db.query(Country)
        if region:
            query = query.filter(Country.region == region)
        if currency:
            query = query.filter(Country.currency_code == currency)
        if sort:
            parts = sort.split("_")
            if len(parts) == 2:
                field, direction = parts
                col = None
                if field == "gdp":
                    col = Country.estimated_gdp
                elif field == "population":
                    col = Country.population
                elif field == "name":
                    col = Country.name
                if col:
                    if direction == "desc":
                        query = query.order_by(desc(col))
                    elif direction == "asc":
                        query = query.order_by(asc(col))
        return query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})




@router.get("/countries/image")
async def get_image():
    """Serve the summary image."""
    image_path = "cache/summary.png"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail={"error": "Summary image not found"})
   

@router.get("/countries/{name}", response_model=CountryOut)
def get_country(name: str, db: Session = Depends(get_db)):
    """Retrieve details of a specific country by name."""
    country = db.query(Country).filter(func.lower(Country.name) == name.lower()).first()
    if not country:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    return country
    
    
@router.delete("/countries/{name}")
def delete_country(name: str, db: Session = Depends(get_db)):
    """Delete a specific country by name."""
    try:
        country = db.query(Country).filter(func.lower(Country.name) == name.lower()).first()
        if country:
            db.delete(country)
            db.commit()
        return {"message": "Deletion attempted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})


@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    """Get status of the countries data."""
    try:
        total = db.query(func.count(Country.id)).scalar()
        last_refresh = db.query(func.max(Country.last_refreshed_at)).scalar()
        return {
            "total_countries": total,
            "last_refreshed_at": last_refresh.isoformat() if last_refresh else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})

