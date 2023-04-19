from sqlalchemy import Column, Boolean, String, Integer, UUID, Float, ForeignKey, func
from geoalchemy2 import Geography, WKTElement
import uuid
from database import Base
from sqlalchemy.orm import Session
from database import engine
from models.Opinion import Opinion
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


class Place(Base):
    __tablename__ = "place"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, server_default='FALSE', nullable=False, default=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geography('POINT', srid=4326, spatial_index=True), nullable=False)
    category = Column(String, ForeignKey('category.category', ondelete="CASCADE"))

    def __init__(self, name, description, published, latitude, longitude, category):
        self.name = name
        self.description = description
        self.published = published
        self.latitude = latitude
        self.longitude = longitude
        self.category = category
        self.location = WKTElement(f'POINT({longitude} {latitude})', srid=4326)

    @hybrid_property
    def avg_score(self):
        session = Session()
        avg = session.query(func.avg(Opinion.stars)).filter(Opinion.place == self.id).one()
        session.close()
        if str(avg[0])=='None':
            return float(0.0)
        else:
            return float(avg[0])

