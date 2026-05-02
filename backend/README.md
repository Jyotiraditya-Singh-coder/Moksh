EduNex AI – Backend Microservices
Welcome to the EduNex AI backend – a production‑ready, microservices‑based platform for AI‑powered education.
All services are containerized with Docker and orchestrated via Docker Compose.
The system is fully open‑source and uses free APIs (Groq, Hugging Face Inference) where possible.

📚 Table of Contents
Architecture Overview

Services

Databases & Storage

Quick Start

Environment Variables

API Documentation

License

🏗️ Architecture Overview
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                             API Gateway (Node.js)                           │
│                           Port 3000 – JWT Auth, Routing                     │
└───────────────────────────────┬─────────────────────────────────────────────┘
        │            │           │           │           │           │
        ▼            ▼           ▼           ▼           ▼           ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Dropout      │ │ Question     │ │ Skill Gap    │ │ Voice Tutor  │
│ Prediction   │ │ Engine       │ │ Analyzer     │ │ (Whisper+Groq)│
│ Port 8001    │ │ Port 8002    │ │ Port 8003    │ │ Port 8004    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Optimization │ │ Recommendation│ │ Explanation  │ │ Subject      │
│ Engine       │ │ Engine       │ │ Generator    │ │ Training     │
│ (OR‑Tools)   │ │ (Surprise)   │ │ (Flan‑T5)    │ │ Engine       │
│ Port 8005    │ │ Port 8006    │ │ Port 8007    │ │ Port 8008    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Skill        │ │ Quant Mentor │ │ Content      │ │ Collaboration│
│ Navigator    │ │ (Knowledge   │ │ Authoring    │ │ Engine       │
│ (KT+Graph)   │ │  Graph)      │ │ (Groq+gTTS)  │ │ (WebRTC)     │
│ Port 8009    │ │ Port 8010    │ │ Port 8011    │ │ Port 8012    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
┌──────────────┐ ┌──────────────┐
│ Resource     │ │ DSA Trainer  │
│ Scraper      │ │ (Groq + Mongo)│
│ (Scrapy)     │ │ Port 8014    │
│ Port 8013    │ └──────────────┘
└──────────────┘
        │            │
        └────────────┴───────────┴───────────┴───────────┴───────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Shared Infrastructure                               │
│  ┌──────────┐  ┌────────┐  ┌──────────┐  ┌─────────┐  ┌─────────────┐    │
│  │ MongoDB  │  │ Redis  │  │  MLflow  │  │Airflow │  │  FAISS      │    │
│  │ (profiles│  │(cache) │  │(registry)│  │(scheduler)│  │(vectors)   │    │
│  │ history) │  │        │  │          │  │         │  │             │    │
│  └──────────┘  └────────┘  └──────────┘  └─────────┘  └─────────────┘    │
│                                   PostgreSQL                               │
│                                   (Airflow metadata)                       │
└─────────────────────────────────────────────────────────────────────────────┘
🧩 Services
Service	Port	Description	Key Technologies
Gateway	3000	API gateway – authentication, routing, rate limiting	Node.js, Express, JWT, MongoDB
Dropout Prediction	8001	ML model (XGBoost) predicting dropout risk with SHAP explanations; auto‑retrained via API	Python, FastAPI, XGBoost, SHAP, MLflow
Question Engine	8002	Groq‑powered adaptive question generation (multilingual)	Python, FastAPI, Groq
Skill Gap Analyzer	8003	Resume parsing, skill extraction, FAISS job matching; allows adding custom job roles	Python, FastAPI, Sentence‑Transformers, FAISS
Voice Tutor	8004	Whisper speech‑to‑text + Groq explanation (multilingual)	Python, FastAPI, Whisper, Groq
Optimization Engine	8005	OR‑Tools based study plan optimization	Python, FastAPI, OR‑Tools
Recommendation Engine	8006	Collaborative filtering (Surprise) for personalised question recommendations	Python, FastAPI, Surprise, MLflow
Explanation Generator	8007	Natural language explanations using Flan‑T5 (open‑source)	Python, FastAPI, Hugging Face Transformers
Subject Training Engine	8008	Problem generation, solution analysis, mathematical validation, approach embeddings (FAISS)	Python, FastAPI, Groq, SymPy, FAISS
Skill Navigator	8009	Learner profiling, knowledge tracing, career readiness analysis	Python, FastAPI, scikit‑learn, MLflow
Quant Mentor	8010	Quant trading career guide with knowledge graph and Groq	Python, FastAPI, NetworkX, Groq
Content Authoring	8011	AI co‑pilot for lesson generation (Groq), text‑to‑speech (gTTS), skill taxonomy (FAISS)	Python, FastAPI, Groq, gTTS, FAISS
Collaboration Engine	8012	Real‑time whiteboard (WebSocket), group formation, emotion detection (Hugging Face)	Python, FastAPI, Socket.IO, aiortc, Hugging Face
Resource Scraper	8013	Scrapy‑based web scraping for learning resources (free & paid)	Python, Scrapy, FastAPI
DSA Trainer	8014	Complete DSA learning environment: problem generation, solution analysis, progress tracking, trending topics	Python, FastAPI, Groq, MongoDB
MLflow	5000	Model registry and tracking for all ML services	MLflow, SQLite
Airflow	8080	Workflow scheduler for model retraining	Apache Airflow, PostgreSQL
🗄️ Databases & Storage
Component	Technology	Purpose
Primary database	MongoDB	Stores user profiles, learning history, daily questions, predictions, analysis results, DSA progress
Cache	Redis	Rate limiting, temporary session data, caching of frequent queries
Airflow metadata	PostgreSQL	Stores Airflow DAG runs, task instances, and connections
MLflow	SQLite (local)	Tracks model parameters, metrics, and artifacts; can be switched to PostgreSQL for production
Vector indexes	FAISS	Binary files stored on disk (persisted via Docker volumes):
- skill-gap-analyzer/job_index.faiss – job role embeddings
- subject-training-engine/knowledge_index.faiss – student approach embeddings
- content-authoring/skill_index.faiss – skill taxonomy
All persistent data (MongoDB, PostgreSQL, FAISS files, MLflow DB) are stored in Docker volumes, ensuring data survives container restarts.

🚀 Quick Start
Clone the repository

bash
git clone <your-repo-url>
cd edunex-ai
Create a .env file in the project root

env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token   # optional (for emotion detection / image generation)
JWT_SECRET=your_jwt_secret
RAPIDAPI_KEY=your_rapidapi_key    # if using Udemy API in resource-scraper (optional)
Start all services

bash
docker-compose up --build
Access the gateway at http://localhost:3000
MLflow UI: http://localhost:5000
Airflow UI: http://localhost:8080 (login: airflow / airflow)

🔐 Environment Variables
Variable	Description	Required By
GROQ_API_KEY	Groq API key for LLM services	question‑engine, voice‑tutor, subject‑training‑engine, quant‑mentor, content‑authoring, dsa‑trainer
HF_TOKEN	Hugging Face token (optional)	collaboration‑engine (emotion detection), content‑authoring (image generation)
JWT_SECRET	Secret for JWT signing	gateway
RAPIDAPI_KEY	RapidAPI key for Udemy API (optional)	resource‑scraper
MLFLOW_TRACKING_URI	(internal) default http://mlflow:5000	all ML services
All other configurations are defined in docker-compose.yml and per‑service .env files.

📚 API Documentation
Each service has its own OpenAPI (Swagger) docs available at http://<service>:<port>/docs when running locally.
The gateway does not provide a combined Swagger UI, but you can explore each service individually.

Main gateway endpoints (prefix /api):

/auth/* – registration, login

/student/* – profile management

/questions/* – daily adaptive questions

/ml/* – dropout prediction & fine‑tuning

/career/* – skill gap analysis, job role management

/voice/* – voice tutor

/optimize/* – study plan optimization

/subject/* – subject training engine

/skill-navigator/* – learner profiling, paths, career readiness

/quant-mentor/* – quant trading guides, knowledge graph

/content-authoring/* – lesson generation, skill taxonomy

/collaboration/* – group formation, emotion detection

/resources/* – learning resource suggestions (Scrapy)

/dsa/* – DSA problem generation, analysis, trending topics

/fine-tune/* – model fine‑tuning (teacher/admin only)

Detailed request/response examples are provided in the respective service documentation.

