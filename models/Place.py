from sqlalchemy import Column, Boolean, String, Integer, UUID, Float, ForeignKey
from geoalchemy2 import Geography, WKTElement
import uuid
from database import Base
from models.Category import Category
from sqlalchemy.orm import relationship


class Place(Base):
    __tablename__ = "place"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, server_default='FALSE', nullable=False, default=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geography('POINT', srid=4326, spatial_index=True), nullable=False)
    # created_by = relationship(User)
    category = Column(String, ForeignKey('category.category', ondelete="CASCADE"))

    def __init__(self, name, description, published, latitude, longitude, category):
        self.name = name
        self.description = description
        self.published = published
        self.latitude = latitude
        self.longitude = longitude
        self.category = category
        self.location = WKTElement(f'POINT({longitude} {latitude})', srid=4326)