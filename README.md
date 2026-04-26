# MMA Coach Web Application - AI-Powered Fight Analysis

An intelligent web application that analyzes Muay Thai sparring footage and provides detailed coaching feedback on technique, footwork, and strategy.

## 🎯 Problem

Amateur fighters need constructive technique feedback but lack access to affordable coaching. Traditional video review is time-consuming and requires expert knowledge.

## 💡 Solution

Automated AI-powered video analysis that identifies strengths, weaknesses, and areas for improvement in real-time fight, sparring, or training footage.

## ✨ Features

- **Video Upload & Management** - Cloud storage with instant playback
- **General Fight Analysis** - Overall performance assessment across entire bout
- **Timestamped Breakdown** - Detailed analysis of specific sequences
- **Technique Identification** - Fighters identified by glove color
- **Actionable Feedback** - Concrete suggestions for improvement

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React** - UI components and state management
- **Tailwind CSS** - Styling

### Backend
- **Python 3.11** - Core backend logic
- **FastAPI** - RESTful API endpoints
- **OpenCV** - Video processing and frame extraction
- **LLaVA 7B** - Local vision-language model for analysis
- **Ollama** - LLM runtime

### Infrastructure
- **Supabase** - PostgreSQL database for metadata and analysis results
- **Cloudflare R2** - S3-compatible object storage for videos
- **Local-first Architecture** - Zero cloud compute costs

## 🏗️ Architecture
```
User → Next.js Frontend (localhost:3000)
         ↓
    FastAPI Backend (localhost:8000)
         ↓
    ┌────┴────┬─────────┬──────────┐
    ↓         ↓         ↓          ↓
  OpenCV   LLaVA   Supabase   Cloudflare R2
  (Frames) (AI)   (Metadata)  (Videos)
```

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

## 📊 Analysis Pipeline

1. **Video Upload** → Stored in Cloudflare R2
2. **Metadata Extraction** → Duration, FPS, format saved to Supabase
3. **Frame Extraction** → OpenCV extracts key frames
4. **AI Analysis** → LLaVA processes frames with coaching prompt
5. **Result Storage** → Feedback saved to Supabase
6. **Display** → Results rendered in interactive UI

## 🚀 Getting Started

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

**2. Install Ollama and pull LLaVA**
```bash
ollama pull llava:7b
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

## 📖 Usage

1. **Upload Video** - Select and upload sparring footage (.mp4, .mov)
2. **Select Video** - Choose from uploaded videos
3. **General Analysis** - Click "Analyze Displayed Video" for full fight assessment
4. **Timestamp Analysis** - Enter start/end times for specific sequence analysis
5. **View Results** - Toggle summaries to view detailed feedback

## 🔍 Example Analysis Output

**General Summary:**
> Fighter in red gloves demonstrates strong orthodox stance with good guard positioning throughout rounds 1-2. Jab technique is crisp with proper hip rotation. However, footwork becomes flat-footed in later rounds, reducing mobility. Recommend: Circle more after combinations, maintain lighter stance on balls of feet.

**Timestamp Analysis (0:30 - 1:00):**
> Excellent 1-2-low kick combination at 0:42. Lead hand returns to guard immediately after jab. Rear cross shows good weight transfer. Low kick lands clean with proper hip turnover. To improve: Add head movement after the cross to avoid counter right hand.

## ⚡ Performance

- **Frame Extraction:** ~2-3 seconds for 50 frames
- **AI Analysis (LLaVA 7B on CPU):** ~4-6 minutes for 50 frames
- **Total Pipeline:** 5-8 minutes per video (CPU)

## 🎓 Learnings & Iterations

### Iteration 1: Architecture Selection
- **Challenge:** Balance between cost, speed, and quality
- **Decision:** Local-first with LLaVA for MVP, Claude Vision for production
- **Result:** Zero ongoing costs, acceptable quality for demonstration

### Iteration 2: Frame Extraction
- **Initial Approach:** 50 frames per video
- **Issue:** LLaVA context overload, slow processing
- **Solution:** Reduced to 10-15 frames for general analysis, 20-30 for timestamps
- **Impact:** 60% faster processing, maintained analysis quality

### Iteration 3: User Feedback
- **Testing:** 3 fighters from local gym
- **Feedback:** "Generic observations" vs "actionable technique advice"
- **Fix:** Refined prompts to focus on specific techniques (stance, combinations, defense)
- **Result:** Improved perceived usefulness

## 🔮 Future Enhancements

- **Claude Vision Integration** - Premium tier with superior analysis quality
- **Video Trimming** - In-app editing before analysis
- **Comparison Mode** - Side-by-side analysis of multiple sessions
- **Progress Tracking** - Track improvement over time
- **Mobile App** - React Native for on-the-go recording and analysis

## 🤔 Technical Tradeoffs

### LLaVA vs Claude Vision

| Factor | LLaVA 7B | Claude Vision |
|--------|----------|---------------|
| Cost | Free | ~$0.10-0.50/video |
| Speed | 5-8 min (CPU) | 30-60 sec |
| Quality | Good | Excellent |
| Privacy | 100% local | API request |
| Use Case | MVP/Free tier | Production/Premium |

**Decision:** Ship MVP with LLaVA, offer Claude as paid upgrade in the future.

## 📝 Lessons Learned

1. **Local LLMs have real limitations** - Quality vs cost tradeoff is real
2. **Frame selection matters more than quantity** - 15 well-chosen frames > 50 sequential
3. **User testing drives improvement** - Real fighters provided invaluable feedback
4. **MVP scope discipline** - Resisted feature creep, shipped working product

## 👤 Author

**Alexander Furst**
- LinkedIn: [Alexander Furst](https://linkedin.com/in/alexfurst)

---

**Built as an independent project for West Chester University of Pennsylvania Computer Science program, Spring 2026**
