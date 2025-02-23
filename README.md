# Video Retrieval System 🌟

**A Smart System for Automated News Event Retrieval from Video Streams**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) 
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/) 
[![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900)](https://aws.amazon.com/) 
[![Gradio](https://img.shields.io/badge/UI-Gradio-FF6B6B)](https://gradio.app/)

---

## 📖 Project Overview

This project aims to build an intelligent system for retrieving specific news events from daily news videos. Designed for scalability, it automatically processes new YouTube video updates, extracts keyframes, generates embeddings using AI models, and provides a user-friendly search interface. 

**Core Features**:
- 🎥 **Automated Video Ingestion**: Auto-download new videos from YouTube channels.
- 🔑 **Keyframe Extraction**: Identify meaningful frames using advanced algorithms.
- 🧠 **AI-Powered Embeddings**: Utilize CLIP model for semantic image/text understanding.
- ☁️ **Cloud-Native Architecture**: Leverage AWS EC2/S3 for scalable storage and processing.
- 🤖 **Workflow Automation**: Orchestrated via n8n and Kaggle pipelines.

---

## 🖼️ System Architecture

![Image](https://github.com/user-attachments/assets/e03fb571-a35a-4f7f-866f-c802257c4920)
**n8n pipeline**
![Image](https://github.com/user-attachments/assets/03684ce6-03e3-42b8-90da-73128867974e)
---

## 🛠️ Tech Stack

| Category          | Technologies/Tools                                                                 |
|-------------------|-----------------------------------------------------------------------------------|
| **Core Platform** | Python, FastAPI, Gradio                                                           |
| **Automation**    | n8n, Kaggle API, Bash Scripting                                                   |
| **AI/ML**         | CLIP (OpenAI), Keyframe Detection Algorithms                                      |
| **Cloud**         | AWS EC2 (Deployment), S3 (Storage), IAM (Credentials)                             |
| **DevOps**        | Docker, Docker Compose                                                            |

---

## 🚀 Key Components

### 1. Automated Pipeline
- **YouTube Monitoring**: n8n workflows trigger on new video uploads.
- **Video Processing**: 
  - Kaggle kernels for batch processing (keyframe extraction + embeddings).
  - Integration with AWS S3 for raw video storage.
- **Database Updates**: Processed embeddings stored in vector DB.

### 2. AI Engine
- **CLIP Model**: Generates multimodal embeddings for text-image retrieval.
- **Keyframe Selection**: Optimized algorithm to reduce redundancy.

### 3. User Interface
- **Gradio App**: Search events using text queries or example images.
- **FastAPI Backend**: Handles search logic and DB interactions.

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- AWS Account (EC2 + S3)
- Kaggle API Token
- Docker & Docker Compose

### Quick Start (AWS EC2)
```bash
# Connect to EC2 instance
ssh -i "your-key.pem" ubuntu@ec2-instance-address

# Clone repo & setup environment
git clone https://github.com/your-repo/video-retrieval.git
cd video-retrieval
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure AWS credentials
aws configure
export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"

# Start services
docker-compose up -d  # Launches n8n, FastAPI, Gradio
```

---
## 📺 User Interface
![Image](https://github.com/user-attachments/assets/908ee7e4-f823-48b3-9749-f4729a83893c)

## 🕑 Development Progress

| Component               | Status     | Details                                                                 |
|-------------------------|------------|-------------------------------------------------------------------------|
| YouTube Auto-Download   | ✅ Complete | n8n triggers + manual credential setup                                 |
| Keyframe Extraction     | ✅ Complete | Tested with Kaggle pipeline                                            |
| CLIP Embeddings         | 🚧 In Progress | Integrating with FastAPI backend                                       |
| AWS S3 Integration      | ✅ Complete | Video storage operational                                              |
| Gradio UI               | 🚧 In Progress | Basic search interface implemented                                     |

---

## 📚 References & Credits

- **Kaggle API**: [Official Documentation](https://www.kaggle.com/docs/api)
- **n8n Automation**: [YouTube Integration Guide](https://n8n.io/integrations/youtube)
- **CLIP Model**: [OpenAI's CLIP Paper](https://arxiv.org/abs/2103.00020)
- **AWS Setup**: [EC2 Deployment Tutorial](https://aws.amazon.com/getting-started/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---