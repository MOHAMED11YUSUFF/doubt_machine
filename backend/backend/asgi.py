import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapis.main import app as fastapi_app

from starlette.middleware.wsgi import WSGIMiddleware
from starlette.applications import Starlette
from starlette.routing import Mount

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_app = get_asgi_application()

application = Starlette(
    routes=[
        Mount("/api", fastapi_app),   # FastAPI endpoints
        Mount("/", django_app),       # Django endpoints
    ]
)