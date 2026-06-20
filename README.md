# 🏥 Healthcare AI Command Center

## LangGraph + Multi Agent AI Healthcare Automation Platform


![Healthcare AI](docs/architecture.png)


## 🚀 Overview

Healthcare AI Command Center is an enterprise-style
Agentic AI platform built using:

- LangGraph
- LangChain
- FastAPI
- Streamlit
- RAG
- n8n Automation


The platform demonstrates how multiple AI agents
collaborate to automate healthcare workflows.



---

# ✨ Features


## 🤖 Multi Agent Architecture


The system contains specialized AI agents:


| Agent | Responsibility |
|---|---|
| Patient Agent | Patient interaction |
| Clinical Agent | Diagnosis workflow |
| Medical RAG Agent | Medical knowledge retrieval |
| Insurance Agent | Coverage & claims |
| Billing Agent | Invoice automation |
| Pharmacy Agent | Medication workflow |
| Operations Agent | Hospital management |
| Safety Agent | AI guardrails |



---

# 🧠 LangGraph Workflow


```
User Query

      |
      v

Patient Coordinator Agent

      |
      v

LangGraph Router

      |
      +----------------+
      |                |
      v                v

Clinical Agent     Insurance Agent

      |
      v

Medical RAG

      |
      v

Billing / Pharmacy

      |
      v

Safety Guardrails

```



---

# 🎙 Voice Healthcare Assistant


Features:

- Speech to Text using Whisper
- AI health assistant
- Voice based patient interaction



---

# 🏥 Hospital Dashboard


Includes:

- Doctor monitoring
- Patient analytics
- AI agent monitoring
- Hospital operations dashboard



---

# 🔥 Automation


Integrated with n8n:


### Appointment Automation

- Doctor booking
- Patient email notification


### Insurance Automation

- Claim creation
- Claim notification


### Billing Automation

- Invoice generation
- Email delivery



---

# 🛠 Tech Stack


Backend:

- FastAPI
- LangGraph


Frontend:

- Streamlit


AI:

- LangChain
- OpenAI
- groq


Automation:

- n8n



---

# ▶ Run Locally


Clone:


```bash
git clone YOUR_REPOSITORY_URL
```


Install:


```bash
pip install -r requirements.txt
```


Create `.env`


Run backend:


```bash
uvicorn backend:app --reload
```


Run frontend:


```bash
streamlit run frontend.py
```



---

# 📂 Project Structure


```
agents/
backend.py
frontend.py
graph.py
tools.py
requirements.txt
```


---

# ⚠️ Disclaimer

This project is an AI healthcare assistant prototype.

It does not replace professional medical advice.


---

## 👨‍💻 Built With

LangGraph + LangChain + FastAPI + Streamlit


## AI Agentic Healthcare Platform