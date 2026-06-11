from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db, seed_demo_data

from app.routers.users import router as users_router
from app.routers.courses import router as courses_router
from app.routers.tests import router as tests_router
from app.routers.profile import router as profile_router
from app.routers.integration import router as integration_router
from app.routers.pages import router as pages_router

app = FastAPI(
    title="Online Courses Platform",
    description="Course project for design patterns with manual implementation of patterns",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup():
    init_db()
    seed_demo_data()

app.include_router(users_router)
app.include_router(courses_router)
app.include_router(tests_router)
app.include_router(profile_router)
app.include_router(integration_router)
app.include_router(pages_router)
