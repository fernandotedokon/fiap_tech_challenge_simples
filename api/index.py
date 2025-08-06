# api/index.py
from fastapi import FastAPI
from main import app as fastapi_app
from mangum import Mangum

# Adaptador ASGI para ambiente serverless
handler = Mangum(fastapi_app)
