def grader_episode(state, total_reward):

    if state.landed:
        score = 0.95   # ✅ never 1.0

        if state.fuel < 20:
            score -= 0.2

        if abs(state.vy) > 0.5:
            score -= 0.3

        # ✅ clamp strictly between (0,1)
        return max(0.01, min(0.99, score))

    elif state.crashed:
        return 0.01   # ✅ not 0.0

    # default case
    return 0.3
