# MMA Coach Web Application - AI-Powered Fight Analysis

An intelligent web application that analyzes Muay Thai sparring footage and provides detailed coaching feedback on technique, footwork, and strategy.

## Problem

Amateur fighters need constructive technique feedback but lack access to affordable coaching. Traditional video review is time-consuming and requires expert knowledge.

## Solution

I created an MMA Coaching Web-App that can analyze different types of combat sport footage ranging from amateur and professional fight, sparring, padwork, and training footage, ranging from the sports of MMA, Muay Thai Kickboxing, Dutch Kickboxing, and traditional Boxing. 

## Features

- **Video Upload & Management** - Cloud video and metadata storage with instant playback - stores your videos, info about each video, and your AI analyses.
- **General Fight Analysis** - Overall performance assessment across entire video
- **Timestamped Breakdown** - Detailed analysis of specific sequences, user can choose start and end point of subclip.
- **Actionable Feedback** - Provides strenghts, weaknesses, and areas to improve on for each fighter.
- **User Friendly UX** - Friendly browser user interface for non-technical users

## Constraints

- Zero budget
- 16 weeks to complete MVP
- Everything locally hosted had to run on my laptop, with only 16 GB RAM and only a CPU

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React** - UI components and state management

### Backend
- **Python 3.13.11** - Core backend logic
- **FastAPI** - RESTful API endpoints
- **OpenCV** - Video processing and frame extraction
- **LLaVA 7B** - Local vision-language model for analysis
- **Llama3.1 8B** - Local LLM model for aggregating LlaVa responses into single cohesive response
- **Ollama** - LLM runtime

### Infrastructure
- **Supabase** - PostgreSQL database for metadata and analysis results
- **Cloudflare R2** - S3-compatible object storage for videos
- **Local-first Architecture** - Zero cloud compute costs

### Key Design Decisions

**Local-First Processing**
- Videos processed on user's machine
- Zero cloud compute costs
- Privacy-preserving (videos never leave local storage during analysis)

**Frame Extraction Strategy**
- Extract 10-50 evenly-spaced frames per analysis
- Reduces processing time while maintaining context
- Configurable based on video duration

**AI Model Selection**
- LLaVA 7B chosen for MVP (free, local inference)
- Claude Vision API ready for production upgrade
- Documented quality-cost tradeoff

## Analysis Pipeline

1. **Video Upload** → Stored in Cloudflare R2
2. **Metadata Extraction** → Duration, FPS, format saved to Supabase
3. **Frame Extraction** → OpenCV extracts key frames
4. **AI Analysis** → LLaVA processes frames with coaching prompt
5. **Result Storage** → Feedback saved to Supabase
6. **Display** → Results rendered in interactive UI

## Getting Started

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.11+**
- **Ollama** - [Install from ollama.ai](https://ollama.ai)
- **Supabase Account** - [supabase.com](https://supabase.com)
- **Cloudflare R2** - [cloudflare.com/r2](https://www.cloudflare.com/products/r2/)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/mma-coach.git
cd mma-coach
```

**2. Install Ollama and pull models**
```bash
ollama pull llava:7b
ollama pull llama3.1:8b
```

**3. Backend setup**
```bash
pip install -r requirements.txt
```

**4. Frontend setup**
```bash
cd frontend
npm install
```

**5. Environment variables**

Create `.env` in backend directory:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_ACCESS_KEY_ID=your_access_key
CLOUDFLARE_SECRET_ACCESS_KEY=your_secret_key
CLOUDFLARE_BUCKET_NAME=your_bucket_name
```

**6. Database setup**

Run the SQL schema from `backend/schema.sql` in your Supabase SQL editor.

### Running the Application

**Terminal 1 - Backend:**
```bash
uvicorn api.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000`

## Usage

1. **Upload Video** - Select and upload sparring footage (.mp4, .mov)
2. **Select Video** - Choose from uploaded videos
3. **General Analysis** - Click "Analyze Displayed Video" for full fight assessment
4. **Timestamp Analysis** - Enter start/end times for specific sequence analysis
5. **View Results** - Toggle summaries to view detailed feedback

## Example Analysis Output

**General Summary:**
> Fighter in red gloves demonstrates strong orthodox stance with good guard positioning throughout rounds 1-2. Jab technique is crisp with proper hip rotation. However, footwork becomes flat-footed in later rounds, reducing mobility. Recommend: Circle more after combinations, maintain lighter stance on balls of feet.

**Timestamp Analysis (0:30 - 1:00):**
> Excellent 1-2-low kick combination at 0:42. Lead hand returns to guard immediately after jab. Rear cross shows good weight transfer. Low kick lands clean with proper hip turnover. To improve: Add head movement after the cross to avoid counter right hand.


## Future Enhancements

- **Premium Vision Model Integration** - Adding optionality to use paid LLMs and LVMs with API call
- **Pose Estimation** - Using YOLOv8 or similar technology to track each fighter's movements better before sending to analysis for increased accuracy
- **Progress Tracking and Logging** - Track improvement over time using RAG
- **Mobile App** - React native to allow for easy uploads and analysis

## Technical Tradeoffs

- Using paid models is very expensive. I had zero budget to operate with, so I chose to host models locally. Unfortunately, this heavily affected the project. LlaVa 7B is very weak for image analysis. It hallucinates things, mixes up which fighter is which, and takes forever to run on my laptop (HP Envy). I think this application would be so much better if I was able to use Claude Vision or something similar.

## 👤 Author

**Alexander Furst**
- LinkedIn: [Alexander Furst](https://linkedin.com/in/alexfurst)

---

**Built as an independent project for West Chester University of Pennsylvania Computer Science program, Spring 2026**
