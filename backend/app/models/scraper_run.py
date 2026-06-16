from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ScraperRun(Base):
    __tablename__ = 'scraper_runs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scraper_name: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(20), default='success')
    message: Mapped[str] = mapped_column(String(500), default='')
    records_collected: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
