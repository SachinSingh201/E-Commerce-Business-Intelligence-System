from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.segmentation_service import SegmentationService

router = APIRouter()

@router.get("/segmentation")
def get_customer_segmentation(clusters: int = 4, db: Session = Depends(get_db)):
    return SegmentationService.perform_rfm_segmentation(db, n_clusters=clusters)

@router.get("/latest")
def get_latest_customers(limit: int = 100, db: Session = Depends(get_db)):
    return SegmentationService.get_latest_customers(db, limit=limit)
