from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.env import SpaceCraftEnv
from src.models import Action

app = FastAPI()
env = SpaceCraftEnv()

# ---------------- SERVE FRONTEND ---------------- #

# Mount static folder (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve UI on root "/"
@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


# ---------------- API ENDPOINTS ---------------- #

@app.get("/reset")
def reset(task: str = "easy"):
    return env.reset(task).dict()


@app.post("/step")
def step(action: Action):  # ✅ use model instead of dict
    result = env.step(action)
    return result.dict()


@app.get("/state")
def get_state():
    return env.state.dict()