import uvicorn
import fastapi

from uvicorn.config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=1
)


@app.get("/", status_code=200, response_class=fastapi.responses.JSONResponse, tags=["STATUS"])
async def root():
    return {"message": "It is working!"}


@app.get("/ping", status_code=200, response_class=fastapi.responses.JSONResponse, tags=["STATUS"])
async def pong():
    return {"ping": "pong!"}


# Only to test.py
def run():

    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)-23s | %(levelname)-8s | %(client_addr)-45s | "%(request_line)s" %(status_code)s'

    config = uvicorn.Config(app=app, host="0.0.0.0", port=5000, reload=False)
    server = uvicorn.Server(config)
    server.run()
