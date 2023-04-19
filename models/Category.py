from sqlalchemy import Column, Boolean, String, Integer, UUID, Float
from geoalchemy2 import Geography, WKTElement
import uuid
from database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    category = Column(String, unique=True, nullable=False)
