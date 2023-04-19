from sqlalchemy import Column, String, UUID, Boolean
import uuid
from database import Base
from sqlalchemy_utils import EmailType



class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(EmailType)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)