from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.v1.schemas.url_scanner import (
    URLScanRequest,
    URLScanResponse
)

from backend.database.connection import get_db
from backend.database.models import ScanHistory, User
from backend.core.dependencies import get_current_user

from ai_engine.risk_engine.risk_engine import calculate_risk


router = APIRouter()


@router.post(
    "/scan/url",
    response_model=URLScanResponse
)
def scan_url(
    request: URLScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = calculate_risk(str(request.url))

    scan_record = ScanHistory(
        url=result["url"],
        risk_level=result["risk_level"],
        risk_score=result["risk_score"],
        reasons=result["reasons"],
        domain=result["domain"],
        user_id=current_user.id
    )

    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)

    return result