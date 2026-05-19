from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.forecast_service import ForecastService

router = APIRouter()

@router.get("/")
def get_forecast(periods: int = 30, db: Session = Depends(get_db)):
    return ForecastService.forecast_sales(db, periods=periods)
