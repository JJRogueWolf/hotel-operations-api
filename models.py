from datetime import datetime

from sqlalchemy import Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Issue(Base):
    __tablename__ = "issues"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )