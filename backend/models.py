from sqlalchemy import Column, Integer, String, Boolean
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    fathers_name = Column(String, nullable=True)
    last_qualification = Column(String, nullable=True)
    register_as_parent = Column(Boolean, default=False, nullable=True)
    cnic_front_path = Column(String, nullable=True)
    cnic_back_path = Column(String, nullable=True)    
    otp_code = Column(String(6), nullable=True)
    is_verified = Column(Boolean, default=False)
