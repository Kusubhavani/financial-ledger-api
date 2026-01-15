from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Ledger API")

app.include_router(router)

@app.get("/")
def health():
    return {"status": "Ledger API running"}
