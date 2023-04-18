from sqlalchemy import Column, Boolean, String, Integer, UUID
import uuid
from database import Base
from sqlalchemy.orm import relationship


class Place(Base):
    __tablename__ = "place"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, server_default='FALSE', nullable=False, default=False)
    # created_by = relationship(User)
