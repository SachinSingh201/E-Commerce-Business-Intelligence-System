from pydantic import BaseModel
from typing import List, Optional

class CustomerSegmentation(BaseModel):
    customer_id: str
    recency: int
    frequency: int
    monetary: float
    cluster: int

class SegmentationResponse(BaseModel):
    data: List[CustomerSegmentation]
