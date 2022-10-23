from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import settings

from apis.base import api_router

from db.session import engine
from db.base import Base


def include_router(app_):
    app_.include_router(api_router)


def configure_static(app_):
    app_.mount('/static', StaticFiles(directory='static'), name='static')


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app_ = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app_)
    configure_static(app_)
    create_tables()
    return app_


app = start_application()
