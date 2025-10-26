from sqlalchemy import func, desc
from PIL import Image, ImageDraw
import os
from sqlalchemy.orm import Session
from .models import Country


async def generate_summary_image(db: Session, now):
    total = db.query(func.count(Country.id)).scalar()
    top5 = db.query(Country).order_by(desc(Country.estimated_gdp)).limit(5).all()

    img = Image.new('RGB', (800, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), f"Total countries: {total}", fill=(0, 0, 0))
    d.text((10, 50), "Top 5 by estimated GDP:", fill=(0, 0, 0))
    for i, c in enumerate(top5):
        gdp_str = f"{c.estimated_gdp:.2f}" if c.estimated_gdp is not None else "N/A"
        d.text((10, 90 + i * 40), f"{i+1}. {c.name}: {gdp_str}", fill=(0, 0, 0))
    d.text((10, 90 + 5 * 40 + 40), f"Last refresh: {now.isoformat()}", fill=(0, 0, 0))

    os.makedirs("cache", exist_ok=True)
    img.save("cache/summary.png")