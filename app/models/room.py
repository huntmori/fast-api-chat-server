import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SQLEnum, DATETIME
)

from app.database import Base
import uuid
from enum import Enum

class RoomType(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

class JoinType(Enum):
    OPEN = "OPEN"
    PASSWORD = "PASSWORD"
    INVITE = "INVITE"

class Room(Base):
    __tablename__ = "rooms"

    idx = Column(
        type_= Integer, primary_key=True
    )
    uid = Column(
        String(255), unique=True, default=lambda: str(uuid.uuid4())
    )

    from_type = Column(String(255), nullable=False)
    from_uid = Column(String(255), nullable=False)

    type = Column(
        SQLEnum(RoomType, name="room_type", native_enum=False),
        nullable=False,
        default= RoomType.PUBLIC
    )
    join_type = Column(
        SQLEnum(JoinType, name="join_type", native_enum=False),
        nullable=False,
        default= JoinType.OPEN
    )
    created_at = Column(
        DATETIME(timezone=True), server_default=sqlalchemy.sql.func.now()
    )
    updated_at = Column(
        DATETIME(timezone=True), onupdate=sqlalchemy.sql.func.now()
    )
