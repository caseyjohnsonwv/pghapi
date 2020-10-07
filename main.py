from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def get_healthcheck():
    return {"Status":"Alive"}
