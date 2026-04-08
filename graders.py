# graders.py

def grader_episode(state, total_reward):
    if state.get("landed", False):
        score = 0.95   # never 1.0
        if state.get("fuel", 100) < 20:
            score -= 0.2
        if abs(state.get("vy", 0)) > 0.5:
            score -= 0.3
        return max(0.01, min(0.99, score))
    elif state.get("crashed", False):
        return 0.01   # not 0.0
    return 0.3
