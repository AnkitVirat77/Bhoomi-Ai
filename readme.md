cd --- change directory
cd .. ------ back to the main directory

cd project ---
cd flask_app
cd fast_api

pip install flask flask-cors mysql-connector-python

python -m uvicorn app:app --reload


pip install pyodbc -- for sql server connection 


python -c "import secrets; print(secrets.token_hex(32))"  --- secret key
pip install authlib --- for gmail login 


# Bhoomi AI 🌱

Bhoomi AI is an AI-powered smart agriculture platform developed to help farmers solve real-world agricultural problems using Generative AI, Machine Learning, and Computer Vision technologies.

The platform integrates an intelligent chatbot powered by Groq LLM, secure authentication systems, and object detection using YOLOv6 to provide smart farming assistance and improve productivity.

---

## 🚀 Features

- 🤖 AI-powered chatbot for farmer assistance
- 🧠 LLM integration using Groq API
- 🔐 Secure Login & Signup Authentication
- 🌐 Google OAuth Authentication
- 🎯 Object Detection using YOLOv6
- 📊 Machine Learning Integration
- ⚡ FastAPI-powered chatbot APIs
- 🗄️ SQL Server Database Integration
- 💻 Responsive frontend using HTML, CSS, and JavaScript

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Flask (Authentication & User Management)
- FastAPI (Chatbot & AI APIs)

### AI/ML Technologies
- Groq LLM API
- YOLOv6
- Machine Learning

### Database
- SQL Server

---

## 📂 Project Structure

```bash
Bhoomi_AI/
│
├── Project/
│   ├── flask_app/
│   ├── chatbot/
│   ├── static/
│   ├── templates/
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── venv/
