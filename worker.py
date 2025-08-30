from database import SessionLocal, HealthCheck, URL
from sqlalchemy.orm import Session
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import time

def get_db_session():
    db = SessionLocal()
    return db


""" id = Column(Integer, primary_key=True, index=True)

url_id = Column(Integer, ForeignKey("urls.id"))

timestamp = Column(DateTime, default=func.now())

is_up = Column(Boolean)

response_time = Column(Float, nullable=True)

status_code = Column(Integer, nullable=True) """

db = get_db_session()
urls = db.query(URL).all()
while True:
    for url in urls:

        target = str(url.address)
        if target.startswith("www."):
            target = "https://" + target

        resp = requests.head(target)
        print(resp)
    time.sleep(60)