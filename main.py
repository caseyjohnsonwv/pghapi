import uvicorn
from fastapi import FastAPI
import env

app = FastAPI()

@app.get("/healthcheck")
def get_healthcheck():
    return {"Status":"Alive"}

if __name__ == '__main__':
    uvicorn.run(app, host=env.HOST_ADDRESS, port=env.HOST_PORT)
