from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CountryOut(BaseModel):
    id: int
    name: str
    capital: Optional[str]
    region: Optional[str]
    population: int
    currency_code: Optional[str]
    exchange_rate: Optional[float]
    estimated_gdp: Optional[float]
    flag_url: Optional[str]
    last_refreshed_at: datetime

    class Config:
        from_attributes = True  # Enables from_orm