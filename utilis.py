from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from models.User import User

from database import get_db, engine

SECRET_KEY = "mysecretkey"
ALGORITHM = "SHA256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Session = sessionmaker(bind=engine)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(hashed_password, password):
    return pwd_context.verify(password, hashed_password)


def get_user(username, password, db: Session):
    session = Session()
    user = session.query(User).filter(username == username)
    if user in None:
        return False
    if verify_password(user.password, password):
        return user
    return False
