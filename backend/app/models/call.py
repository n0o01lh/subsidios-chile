from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PostulationCall(Base):
    __tablename__ = 'postulation_calls'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subsidy_program: Mapped[str] = mapped_column(String(120), index=True)
    region: Mapped[int] = mapped_column(Integer, index=True)
    opening_date: Mapped[date] = mapped_column(Date)
    closing_date: Mapped[date] = mapped_column(Date)
    available_quotas: Mapped[int] = mapped_column(Integer, default=0)
    requirements: Mapped[str] = mapped_column(String(500))
    source_url: Mapped[str] = mapped_column(String(255))
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
