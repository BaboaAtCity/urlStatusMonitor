from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Float, func
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now() ,nullable=True)
    from_ip = Column(String,nullable=True)




class HealthCheck(Base):
    __tablename__ = "health_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    timestamp = Column(DateTime, default=func.now())
    is_up = Column(Boolean)
    response_time = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)
