import random
import numpy as np
from src.models import LanderState, Action, StepResult
from src.physics import update_physics
from src.reward import compute_reward
from src.tasks import TASKS

random.seed(42)
np.random.seed(42)

class SpaceCraftEnv:

    def __init__(self):
        self.state = None
        self.wind = 0

    def reset(self, task = "easy"):
        config = TASKS[task]

        self.wind = config['wind']

        self.state = LanderState(
            x = 0,
            y = config["initial_height"],
            vx = 0,
            vy = 0,
            angle = 0,
            angular_velocity = 0,
            fuel = config["fuel"],
            landed = False,
            crashed = False,
            steps = 0
        )

        return self.state

    def step(self, action: Action):
        self.state.steps += 1

        self.state = update_physics(self.state, action, self.wind)

        reward, done = compute_reward(self.state)

        return StepResult(
            state = self.state,
            reward = reward,
            done = done,
            info = "ok"
        )
    
    def state(self):
        return self.state