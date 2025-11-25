from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="StudentReportBot")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "StudentReportBot API running"}
