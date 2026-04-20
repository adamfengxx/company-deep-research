from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Text, Integer, DateTime, String
from datetime import datetime, timezone
import uuid


class Base(DeclarativeBase):
    pass


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query: Mapped[str] = mapped_column(Text, nullable=False)
    final_report: Mapped[str] = mapped_column(Text, nullable=False)
    llm_call: Mapped[int] = mapped_column(Integer, default=0)
    tool_call: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
