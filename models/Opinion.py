from sqlalchemy import Column, String, Integer, UUID, CheckConstraint, ForeignKey
from geoalchemy2 import Geography, WKTElement
import uuid
from database import Base


class Opinion(Base):
    __tablename__ = "opinion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    stars = Column(Integer, CheckConstraint('stars>0 and stars<=5'), nullable=False)
    opinion = Column(String, nullable=False)
    place = Column(UUID(as_uuid=True), ForeignKey('place.id', ondelete="CASCADE"))
    #TODO timestamp and filter by it