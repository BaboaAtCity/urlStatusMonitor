from database import SessionLocal, HealthCheck, URL
from sqlalchemy.orm import Session
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime

def get_db_session():
    db = SessionLocal()
    return db

db = get_db_session()
urls = db.query(URL).all()
while True:
    for url in urls:

        target = str(url.address)
        if target.startswith("www."):
            target = "https://" + target
        
        resp = requests.head(target)
        respTime = datetime.datetime.now()
        formatted = respTime.strftime("%M %S")
        print( formatted + str(resp))
        print(f"{datetime.datetime.now()}    {resp}")
        if resp:
            is_up = True
        else:
            is_up = False
        healthObj = HealthCheck(url_id = url.id, 
                                timestamp = respTime, 
                                status_code = resp.status_code, 
                                is_up = is_up,
                                response_time = resp.elapsed.total_seconds())
        db.add(healthObj)
        db.commit()
        db.refresh(healthObj)


    print(f"{datetime.datetime.now()}    now sleeping")
    time.sleep(60)