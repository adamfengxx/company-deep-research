from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.session import init_db
from api.routes.research import router as research_router
from api.routes.reports import router as reports_router
from api.routes.email import router as email_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Company Deep Research ", lifespan=lifespan)
app.include_router(research_router)
app.include_router(reports_router)
app.include_router(email_router)


@app.get("/health")
def health():
    return {"status": "ok"}
