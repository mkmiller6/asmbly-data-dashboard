"""SQL Database schema"""

from typing import List
from typing import Optional
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "member"

    neon_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(55))
    last_name: Mapped[str] = mapped_column(String(55))
    email: Mapped[str] = mapped_column(String(255))
    zip_code: Mapped[Optional[int]]
    risk_score: Mapped[Optional[float]]
    emailed: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)
    membership_duration: Mapped[int]


class MembershipCount(Base):
    __tablename__ = "membership_count"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_active_count: Mapped[int]
    acct_signups_count: Mapped[int]
    member_signups_count: Mapped[int]
    churn_count: Mapped[int]
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
