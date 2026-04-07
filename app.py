from fastapi import FastAPI
from src.env import SpaceCraftEnv
from src.models import Action

app = FastAPI()
env = SpaceCraftEnv()

@app.get("/")
def health():
    return {"status":"ok"}

@app.get("/reset")
def reset(task: str = "easy"):
    return env.reset(task).dict()

@app.post("/step")
def step(action: dict):
    result = env.step(Action(**action))
    return result.dict()

@app.get("/state")
def get_state():
    return env.state.dict()
