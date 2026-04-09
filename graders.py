def grader_episode(state, total_reward):
    try:
        if state.get("landed", False):
            score = 0.95
            if state.get("fuel", 100) < 20:
                score -= 0.2
            if abs(state.get("vy", 0)) > 0.5:
                score -= 0.3
        elif state.get("crashed", False):
            score = 0.05
        else:
            score = 0.3

        # ✅ FINAL SAFETY CLAMP
        return max(0.01, min(0.99, float(score)))

    except Exception:
        return 0.01  # NEVER crash
