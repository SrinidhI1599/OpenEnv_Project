from graders import grader_episode

TASKS = {
    "easy": {
        "initial_height": 8,
        "wind": 0.0,
        "fuel": 120,
        "grader": grader_episode   # ✅ ADD THIS
    },
    "medium": {
        "initial_height": 12,
        "wind": 0.02,
        "fuel": 100,
        "grader": grader_episode   # ✅ ADD THIS
    },
    "hard": {
        "initial_height": 15,
        "wind": 0.05,
        "fuel": 80,
        "grader": grader_episode   # ✅ ADD THIS
    }
}
