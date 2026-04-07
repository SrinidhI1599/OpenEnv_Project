# 🚀 OpenEnv Spacecraft Control Agent

An **OpenEnv-compliant spacecraft simulation environment** with a **FastAPI backend** and an **LLM-powered agent** for automated task execution and evaluation. The environment is deployed on **Hugging Face Spaces**, and the agent interacts with it using structured API calls.

---

## 📌 Features

* ✅ OpenEnv specification compliant (`reset`, `step`, `state`)
* ✅ FastAPI-based simulation environment
* ✅ LLM-powered agent using OpenAI client
* ✅ Dockerized deployment (Hugging Face Spaces)
* ✅ Supports multiple tasks (`easy`, `medium`, `hard`)
* ✅ Structured logging for automated evaluation
* ✅ Lightweight & runs within constrained resources

---

## 🏗️ Project Structure

```
.
├── app.py               # FastAPI environment server
├── inference.py        # LLM agent script
├── openenv.yaml        # OpenEnv specification
├── Dockerfile          # HF Space deployment
├── requirements.txt    # Dependencies
├── tasks/              # Task definitions
├── graders/            # Evaluation logic
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv openenv
openenv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
HF_TOKEN=your_api_key
ENV_BASE_URL=https://your-space-name.hf.space
```

---

### 5️⃣ Run the Agent

```bash
python inference.py
```

---

## 🌐 Hugging Face Deployment

This project is deployed using **Docker** on Hugging Face Spaces.

### 🔗 Space URL

```
https://<username>-<space-name>.hf.space
```

### Required Files for Deployment:

* `app.py`
* `Dockerfile`
* `requirements.txt`
* `openenv.yaml`

---

## 🔌 API Endpoints

The environment exposes the following endpoints:

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| GET    | `/reset` | Reset environment |
| POST   | `/step`  | Perform action    |
| GET    | `/state` | Get current state |

---

## 🤖 Agent Workflow

1. Calls `/reset` to initialize environment
2. Uses LLM to decide actions
3. Sends actions via `/step`
4. Receives state + reward
5. Logs steps in structured format
6. Computes final score

---

## 📊 Logging Format

The agent outputs structured logs:

```
[START]

[STEP]
step: 0
action: {...}
reward: 0.5

[END]
final_score: 0.85
```

---

## 📈 Evaluation

* Supports **3+ tasks**
* Each task produces a score in range **0.0 – 1.0**
* Final score = average across tasks

---

## ⚠️ Requirements

* Python 3.10+
* Internet connection (for LLM API)
* Hugging Face Space for environment hosting

---

## 🚧 Future Improvements

* Smarter policy using LLM outputs
* Improved reward shaping
* Visualization dashboard
* Multi-agent support

---

## 👤 Author

**SriNidhi T**

---

## 📄 License

This project is for educational and evaluation purposes.
