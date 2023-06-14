from fastapi import FastAPI

from source.apis.routes import router

app = FastAPI()

app.include_router(router)
