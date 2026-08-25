from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import ScanHistory, User
from backend.core.dependencies import get_current_user
from backend.api.v1.schemas.url_scanner import ScanHistoryResponse


router = APIRouter()


# Get scan history with pagination
@router.get(
    "/scan/history",
    response_model=list[ScanHistoryResponse]
)
def get_scan_history(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scans = (
        db.query(ScanHistory)
        .filter(ScanHistory.user_id == current_user.id)
        .order_by(ScanHistory.scanned_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return scans


# Get a single scan by ID
@router.get(
    "/scan/history/{scan_id}",
    response_model=ScanHistoryResponse
)
def get_scan_by_id(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scan = (
        db.query(ScanHistory)
        .filter(
            ScanHistory.id == scan_id,
            ScanHistory.user_id == current_user.id
        )
        .first()
    )

    if scan is None:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    return scan


@router.delete(
    "/scan/history/{scan_id}"
)
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scan = (
        db.query(ScanHistory)
        .filter(
            ScanHistory.id == scan_id,
            ScanHistory.user_id == current_user.id
        )
        .first()
    )

    if scan is None:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    db.delete(scan)
    db.commit()

    return {
        "message": "Scan deleted successfully",
        "scan_id": scan_id
    }