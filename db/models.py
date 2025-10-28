import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"  # название бд в постгре

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    is_active = Column(Boolean(), default=True)  # удалён/не удалён
    hashed_password = Column(String, nullable=False)
