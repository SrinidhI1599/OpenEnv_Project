def compute_reward(state):
    reward = 0
    done = False

    # Crash condition
    if state.y <= 0:
        if abs(state.vy) < 0.5 and abs(state.angle) < 0.2:
            reward = 100
            state.landed = True
        else:
            reward = -100
            state.crashed = True
        done = True

    # Fuel penality
    reward -= 0.05
    reward -= (100 - state.fuel) * 0.01


    # Out of fuel
    if state.fuel <= 0:
        done = True

    return reward, done