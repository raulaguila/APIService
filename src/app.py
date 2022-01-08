import logging
import uvicorn
import fastapi


app = fastapi.FastAPI()


@app.get("/")
def root():
    logging.info("root request!!")
    return {"Raul:": "Del Aguila"}


if __name__ == "__main__":
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8004, reload=False)
    server = uvicorn.Server(config)
    server.run()
