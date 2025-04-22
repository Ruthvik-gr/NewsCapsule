# 📰 Newscapsule

**Newscapsule** is an AI-powered tech news summarization platform that fetches real-time RSS feeds, condenses each article into ~60-word summaries using advanced NLP models, and presents them in a minimal, user-friendly feed. It's built to help users quickly stay updated with the latest in tech, without the noise.

---

## ✨ Features

### 🔍 Smart RSS Aggregation
- Fetches articles from firstpost tech RSS feeds.
- Uses `rss-parser` to structure raw XML feeds into usable JSON data.

### 🧠 AI Summarization (Langchain + LLM)
- Each fetched article is passed to a Langchain pipeline connected to an LLM (Llama).
- The system extracts key points and rewrites them as ~60-word summaries.
- Summaries are optimized for clarity, accuracy, and readability.

### 🔐 Authentication & Personalization
- Users can sign in using `NextAuth.js` (supports providers like Google, GitHub).
- Logged-in users get access to a personalized news feed.

### 📚 Clean UI/UX
- Built using **Next.js** and **Tailwind CSS**, styled with `framer-motion`.
- Fully responsive layout with smooth transitions and clean typography.
- Iconography powered by **lucide-react**.

### 🧾 Source Link Attribution
- Each summary includes a clickable link to the full original article.

---

## 🧠 Tech Stack Breakdown

### 🖥️ Frontend (Next.js)
- Framework: **Next.js 15.1.6**
- Core Library: **React.js**
- Styling: **Tailwind CSS**, `tailwindcss-animate`, `clsx`, `tailwind-merge`
- UI Components: **Radix UI**, `framer-motion`, `lucide-react`
- Auth: **NextAuth.js**
- State Management: Native React state, with server-side rendering for auth/session handling

### ⚙️ Backend (FastAPI + Langchain)
- API Framework: **FastAPI**
- AI Processing: **Langchain**, integrated with a language model like Llama GPT
- Tasks handled:
  - Fetch RSS content and store it in database
  - Format and return summaries

### 🛢️ Database
- **MongoDB** for storing users, feeds
- Connected through FastAPI backend

---