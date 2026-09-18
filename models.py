from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Issue(Base):
    __tablename__ = "issues"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)