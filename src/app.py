import logging
import uvicorn
import fastapi

from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}



# Only to test.py
def run():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8004, reload=False)
    server = uvicorn.Server(config)
    server.run()
