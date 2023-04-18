from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .api import router
from .settings import setting


origin = [
    f"http://{setting.front_end_host}:{setting.front_end_port}",
    f"http://localhost"
]

app = FastAPI()
app.include_router(router)

