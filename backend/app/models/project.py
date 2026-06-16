from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    region: Mapped[int] = mapped_column(Integer, index=True)
    commune: Mapped[str] = mapped_column(String(120), index=True)
    subsidy_program: Mapped[str] = mapped_column(String(80))
    available_units: Mapped[int] = mapped_column(Integer, default=0)
    min_price_uf: Mapped[float] = mapped_column(Float)
    max_price_uf: Mapped[float] = mapped_column(Float)
    bedrooms: Mapped[int] = mapped_column(Integer, default=2)
    address: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str] = mapped_column(String(255))
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
