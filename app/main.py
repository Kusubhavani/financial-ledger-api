from fastapi import FastAPI
from app.routes import router
from app.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Ledger API")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "Financial Ledger API is running"}
