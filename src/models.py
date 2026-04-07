from pydantic import BaseModel

class LanderState(BaseModel):
    x: float
    y: float
    vx: float
    vy: float
    angle: float
    angular_velocity: float
    fuel: float
    landed: bool
    crashed: bool
    steps: int

class Action(BaseModel):
    thrust: float
    rotate: float

class StepResult(BaseModel):
    state: LanderState
    reward: float
    done: bool
    info: str