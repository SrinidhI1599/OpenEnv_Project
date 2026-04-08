from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.env import SpaceCraftEnv
from src.models import Action

app = FastAPI()
env = SpaceCraftEnv()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

# ✅ SUPPORT BOTH GET + POST
@app.get("/reset")
@app.post("/reset")
def reset(task: str = Query(default="easy")):
    return env.reset(task).dict()

@app.post("/step")
def step(action: Action):
    result = env.step(action)
    return result.dict()

@app.get("/state")
def get_state():
    return env.state.dict()
