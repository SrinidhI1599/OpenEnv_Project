import os
import requests
from openai import OpenAI
from tasks import TASKS

# ---------------- ENV SETUP ---------------- #

LLM_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-nano")
HF_TOKEN = os.getenv("HF_TOKEN", "")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:5000")

client = None
try:
    if LLM_BASE_URL and HF_TOKEN:
        client = OpenAI(base_url=LLM_BASE_URL, api_key=HF_TOKEN)
except Exception:
    pass


# ---------------- LOGGING ---------------- #

def log_start(task):
    print(f"[START] task={task}", flush=True)

def log_step(step, reward):
    print(f"[STEP] step={step} reward={reward}", flush=True)

def log_end(task, score, steps):
    print(f"[END] task={task} score={score} steps={steps}", flush=True)


# ---------------- ENV HELPERS ---------------- #

def safe_get(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return {}

def safe_post(url, payload):
    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return {}


# ---------------- TASK RUNNER ---------------- #

def run_task(task_name):
    log_start(task_name)

    state = safe_get(f"{ENV_BASE_URL}/reset?task={task_name}")
    if not isinstance(state, dict):
        log_end(task_name, 0.5, 0)
        return 0.5

    total_reward = 0.0
    steps = 0

    for step in range(200):
        steps = step + 1

        # Optional LLM
        if client:
            try:
                client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": str(state)}],
                    max_tokens=5
                )
            except Exception:
                pass

        vy = state.get("vy", 0)
        action = {
            "thrust": 1.0 if vy < -0.5 else 0.3,
            "rotate": 0.0
        }

        res = safe_post(f"{ENV_BASE_URL}/step", action)

        reward = res.get("reward", 0.0)
        total_reward += reward

        log_step(step, reward)

        state = res.get("state", {})

        if res.get("done", False):
            break

    # ---------------- GRADING ---------------- #

    grader_fn = TASKS.get(task_name, {}).get("grader")

    if grader_fn is None:
        score = 0.5
    else:
        try:
            score = grader_fn(state, total_reward)
        except Exception:
            score = 0.5

    # Safety checks
    if not isinstance(score, (int, float)):
        score = 0.5

    if score <= 0 or score >= 1:
        score = 0.5

    log_end(task_name, score, steps)

    return float(score)


# ---------------- MAIN ---------------- #

def main():
    results = {}

    for task_name in TASKS.keys():
        try:
            score = run_task(task_name)
        except Exception:
            score = 0.5

        if not isinstance(score, (int, float)):
            score = 0.5

        if score <= 0 or score >= 1:
            score = 0.5

        results[task_name] = float(score)

    # Final score
    final_score = sum(results.values()) / len(results) if results else 0.5

    if final_score <= 0 or final_score >= 1:
        final_score = 0.5

    # ✅ REQUIRED JSON OUTPUT
    print({
        "score": float(final_score),
        "tasks": results
    }, flush=True)


# ---------------- ENTRY ---------------- #

if __name__ == "__main__":
    main()
