from typing import List

from pydantic import BaseModel, HttpUrl


class URLScanRequest(BaseModel):
    url: HttpUrl


class URLScanResponse(BaseModel):
    url: str
    risk_level: str
    risk_score: int
    reasons: List[str]
    domain: str
    
from datetime import datetime
class ScanHistoryResponse(BaseModel):
    id: int
    url: str
    risk_level: str
    risk_score: int
    reasons: List[str]
    domain: str
    scanned_at: datetime