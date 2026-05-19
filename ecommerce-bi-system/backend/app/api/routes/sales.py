from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.sales_service import SalesService

router = APIRouter()

@router.get("/monthly")
def get_monthly_sales(db: Session = Depends(get_db)):
    return SalesService.get_monthly_sales(db)

@router.get("/category")
def get_sales_by_category(db: Session = Depends(get_db)):
    return SalesService.get_sales_by_category(db)
