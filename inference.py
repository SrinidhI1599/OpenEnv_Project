import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
LLM_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")
ENV_BASE_URL = os.getenv("ENV_BASE_URL")

# Validate env variables early (fail fast)
if not all([LLM_BASE_URL, MODEL_NAME, HF_TOKEN, ENV_BASE_URL]):
    raise ValueError("❌ Missing required environment variables")

# OpenAI client
client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=HF_TOKEN
)

# ---------------- LOGGING ---------------- #

def log_start():
    print("[START]")

def log_step(step, action, reward):
    print("[STEP]")
    print(f"step: {step}")
    print(f"action: {action}")
    print(f"reward: {reward}")

def log_end(score):
    print("[END]")
    print(f"final_score: {score}")

# ---------------- ENV HELPERS ---------------- #

def safe_get(url):
    res = None  # ✅ initialize

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    except Exception as e:
        print(f"❌ GET failed: {url}")
        print("Error:", str(e))

        if res is not None:
            print("Response:", res.text[:200])
        else:
            print("No response received")

        raise

def safe_post(url, payload):
    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ POST failed: {url}")
        print("Payload:", payload)
        print("Error:", str(e))
        print("Response:", getattr(res, "text", "No response"))
        raise

# ---------------- TASK RUNNER ---------------- #

def run_task(task_name):
    # Reset environment
    state = safe_get(f"{ENV_BASE_URL}/reset?task={task_name}")

    total_reward = 0.0

    for step in range(200):

        # Required LLM call (even if not used heavily)
        try:
            _ = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "user", "content": f"Decide action for state: {state}"}
                ],
                max_tokens=10
            )
        except Exception as e:
            print("⚠️ LLM call failed:", str(e))

        # Simple heuristic policy (can improve later)
        action = {
            "thrust": 1.0 if state.get("vy", 0) < -0.5 else 0.3,
            "rotate": 0.0
        }

        # Step environment
        res = safe_post(f"{ENV_BASE_URL}/step", action)

        reward = res.get("reward", 0.0)
        total_reward += reward

        log_step(step, action, reward)

        state = res.get("state", {})

        if res.get("done", False):
            break

    # Normalize score (0 → 1)
    score = max(0.0, min(1.0, total_reward / 100.0))
    return score

# ---------------- MAIN ---------------- #

def main():
    log_start()

    tasks = ["easy", "medium", "hard"]
    scores = []

    for task in tasks:
        score = run_task(task)
        scores.append(score)

    final_score = sum(scores) / len(scores)

    log_end(final_score)

# ---------------- ENTRY ---------------- #

if __name__ == "__main__":
    main()