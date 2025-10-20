from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import Base


class ComfortOrm(Base):
    __tablename__ = "comfort"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomsComfortOrm(Base):
    __tablename__ = "rooms_comfort"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    comfort_id: Mapped[int] = mapped_column(ForeignKey("comfort.id"))
