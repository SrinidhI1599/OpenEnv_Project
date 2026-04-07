import math

GRAVITY = -0.05
THRUST_POWER = 0.1
ROTATION_POWER = 0.05

def update_physics(state, action, wind):
    # Apply Rotation
    state.angle += action.rotate * ROTATION_POWER
    state.angular_velocity = action.rotate

    # Apply Thrust
    thrust_x = math.sin(state.angle) * action.thrust * THRUST_POWER
    thrust_y = math.cos(state.angle) * action.thrust * THRUST_POWER

    # Update Velocity
    state.vx += thrust_x + wind
    state.vy += thrust_y + GRAVITY

    # Update position
    state.x += state.vx
    state.y += state.vy

    # Fuel consumption
    state.fuel -= action.thrust * 0.5

    return state
