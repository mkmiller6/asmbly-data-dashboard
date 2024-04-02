"""SQL Database schema"""

# pylint: disable=too-few-public-methods, missing-class-docstring

from typing import List
from typing import Optional
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column,
    relationship,
)

from engine import engine


class Base(MappedAsDataclass, DeclarativeBase):
    """All table objects will be converted to dataclasses"""


class Member(Base):
    __tablename__ = "member"

    zip_code: Mapped[Optional[int]]
    risk_score: Mapped[Optional[float]]
    membership_duration: Mapped[int]
    neon_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(55))
    last_name: Mapped[str] = mapped_column(String(55))
    email: Mapped[str] = mapped_column(String(255))
    emailed: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)


class MembershipCount(Base):
    __tablename__ = "membership_count"

    total_active_count: Mapped[int]
    acct_signups_count: Mapped[int]
    member_signups_count: Mapped[int]
    churn_count: Mapped[int]
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, unique=True)


class EventType(Base):
    __tablename__ = "event_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    instances: Mapped[List["EventInstance"]] = relationship(back_populates="event_type")


class EventInstance(Base):
    __tablename__ = "event_instance"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type_id: Mapped[int] = mapped_column(ForeignKey("event_type.id"))
    date: Mapped[datetime.date] = mapped_column(Date)
    event_type: Mapped["EventType"] = relationship(back_populates="instances")
    member: Mapped[Member] = relationship("Member")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
