# 🎓 Moksh — AI-Powered Education Platform

Moksh is an AI-powered, microservices-based education platform designed to provide intelligent learning, assessment, career, and academic assistance through a collection of specialized AI services.

The platform combines modern web technologies, AI/ML services, containerized infrastructure, and multiple data stores to provide features such as question generation, prediction, content creation, recommendation, voice interaction, document processing, and personalized learning assistance.

---

## 🚀 Overview

Moksh is designed around a **microservices architecture**, where individual AI-powered capabilities are separated into independent services.

The system provides a centralized API Gateway that communicates with specialized services responsible for different educational and AI tasks.

The platform is designed to support:

- AI-powered education
- Personalized learning
- Question generation
- Answer evaluation
- Prediction and analytics
- Content generation
- Career assistance
- Recommendation systems
- Voice-based interaction
- Document and text processing
- Knowledge-graph-based learning
- AI-powered collaboration
- Learning resource discovery

---

## ✨ Key Features

### 🤖 AI-Powered Learning

- AI-generated questions
- Personalized learning assistance
- Adaptive learning workflows
- AI-powered answer analysis
- Learning recommendations
- Educational content generation

### 📝 Assessment & Question Generation

- Dynamic question generation
- Question answering
- Difficulty-based learning
- AI-powered evaluation
- Subject-specific learning assistance

### 📊 Prediction & Analytics

- Student performance prediction
- Learning analytics
- Progress tracking
- AI-powered insights
- Performance-based recommendations

### 🎯 Career Assistance

- Career recommendations
- Job matching
- Resume-related assistance
- Skill analysis
- Career preparation tools

### 📚 Content & Knowledge

- AI-powered content authoring
- Knowledge graph integration
- Educational resource discovery
- Document processing
- Text summarization
- Learning material generation

### 🎙️ Voice & Language

- Speech-to-text capabilities
- Text-to-speech capabilities
- Voice-based interaction
- AI-powered conversational assistance

### 🧠 Advanced AI Capabilities

The platform is designed to integrate multiple AI technologies and models, including:

- OpenAI
- Groq
- Hugging Face
- Sentence Transformers
- Whisper
- gTTS
- FastAPI-based AI services

---

# 🏗️ Architecture

Moksh follows a **microservices architecture**.

```text
                         ┌─────────────────────┐
                         │      Frontend       │
                         │   React / Vite      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     API Gateway     │
                         │      Port 8000      │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
       │ Auth / User  │      │  Prediction  │      │   Question   │
       │   Service    │      │   Service    │      │    Service   │
       └──────────────┘      └──────────────┘      └──────────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AI Services      │
                         │ FastAPI / Python    │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐        ┌────────────┐        ┌────────────┐
        │ OpenAI    │        │   Groq     │        │ HuggingFace│
        └───────────┘        └────────────┘        └────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Databases & Storage │
                         └─────────────────────┘
