from sqlalchemy import Column, String, Integer,UUID, CheckConstraint, ForeignKey, DateTime, func
from geoalchemy2 import Geography, WKTElement
import uuid
from database import Base


class Opinion(Base):
    __tablename__ = "opinion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    stars = Column(Integer, CheckConstraint('stars>0 and stars<=5'), nullable=False)
    opinion = Column(String, nullable=False)
    place = Column(UUID(as_uuid=True), ForeignKey('place.id', ondelete="CASCADE"))
    created_by = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete="SET NULL"))
    created_on = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())
