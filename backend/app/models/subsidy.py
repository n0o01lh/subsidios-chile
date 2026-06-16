from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Subsidy(Base):
    __tablename__ = 'subsidies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    decree: Mapped[str] = mapped_column(String(50))
    target: Mapped[str] = mapped_column(String(150))
    frs_min: Mapped[float] = mapped_column(Float)
    frs_max: Mapped[float] = mapped_column(Float)
    benefit_uf: Mapped[float] = mapped_column(Float)
    required_savings_uf: Mapped[float] = mapped_column(Float)
    max_property_value_uf: Mapped[float] = mapped_column(Float)
    mortgage_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
