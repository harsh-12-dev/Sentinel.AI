from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from backend.database.connection import Base


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, nullable=False)

    risk_level = Column(String, nullable=False)

    risk_score = Column(Integer, nullable=False)

    reasons = Column(JSONB, nullable=False)

    domain = Column(String, nullable=False)

    scanned_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )