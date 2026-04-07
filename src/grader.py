def grader_episode(state, total_reward):
    if state.landed:
        score = 1.0

        if state.fuel < 20:
            score -= 0.2

        if abs(state.vy) > 0.5:
            score -= 0.3

        return max(0.0, score)

    elif state.crashed:
        return 0.0
    
    return 0.3