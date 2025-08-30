from database import SessionLocal, URL, HealthCheck
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


urls = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/urls")
def create_item(url: str, db = Depends(get_db)):
    url_obj = URL(address = url)
    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)
    return {"ok" : True, "Monitoring" : url}


@app.get("/all_urls")
def read_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return urls

@app.get("/url/{url_id}")
def read_url(url_id: int, db: Session = Depends(get_db)):
    url = db.get(URL, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"ok": True}

@app.delete("/url/{url_id}")
def delete_url(url_id: int, db: Session = Depends(get_db)):
    url = db.get(URL, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return {"ok": True}

