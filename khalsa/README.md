# AI Chatbot - Interactive AI Tutor & Knowledge Engine

A single-file Python Streamlit chatbot application designed to teach and answer questions about **Artificial Intelligence, Machine Learning, Deep Learning, and Data Science**.

Features a **Light Minimalist UI** with **Sky Blue and Sprinkle Green** accents, pure black input text, and a sidebar with API integrations, an interactive quiz, an XP rewards tracker, and a short question library.

---

## 🌟 Key Features

### 1. Dual-Intelligence Architecture
- **Built-in Offline AI Knowledge Engine**: Completely free and functions 100% offline without needing API keys or an internet connection. Pre-loaded with answers, real-world analogies, and quiz checks for core AI topics.
- **Live Cloud LLM Integration (Optional)**: Connect your **Google Gemini** or **OpenAI** API keys via the sidebar for dynamic real-time responses.

### 2. Light Minimalist UI/UX
- **Palette**: Clean off-white canvas with **Sky Blue** (`#0ea5e9`, `#0284c7`) and **Sprinkle Green** (`#10b981`, `#059669`) highlights.
- **Top-Left Sidebar Minimizer/Maximizer**: Visible in **black** (`#000000`) for easy sidebar collapsing and expanding.
- **Focused Typing Space**: Pure black text (`#000000`) on a clean input container with a Sky Blue to Sprinkle Green send button (`➔`).
- **Responsive Layout**: Designed as a modern floating card container.

### 3. Sidebar Learning Center
- **🔑 API Key Entries**: Masked input entries for Google Gemini and OpenAI with model selectors (`gemini-1.5-flash`, `gpt-4o-mini`, etc.).
- **🏆 Learning Rewards & XP Tracker**:
  - Earn `+5 XP` for every question asked.
  - Earn `+15 XP` for answering quiz questions correctly.
  - Dynamic badge unlock progression:
    - 🌱 *AI Novice* (0–29 XP)
    - 🧠 *Deep Explorer* (30–59 XP)
    - ⚡ *Neural Architect* (60–99 XP)
    - 🏆 *AI Grandmaster* (100+ XP)
- **🎯 Quick Quiz**: Interactive multiple-choice challenges with instant feedback and XP rewards.
- **📚 Short Questions Library (One-Click Explorers)**:
  - 🤖 **What is AI?**
  - 🍳 **What is ML?**
  - 👁️ **What is DL?**
  - 👥 **What is KNN?**
  - 🧠 **Neural Networks**
  - 🧪 **Turing & Tuning Test**
  - 📜 **History of AI**
  - 🏛️ **Founder of AI**
  - 🩺 **How AI Helps**

---

## 📂 Project Structure

```text
d:\khalsa/
├── api/
│   └── index.py      # Vercel Serverless entrypoint (Zero-timeout, WebSocket-free architecture)
├── .streamlit/
│   └── config.toml   # Streamlit cloud theme configuration
├── chatbot.py        # Streamlit application (for local and Streamlit Cloud)
├── question.txt      # Comprehensive list of all offline-supported questions & topics
├── requirement.txt   # Dependencies file
├── requirements.txt  # Standard dependencies file (includes Flask for Vercel)
├── vercel.json       # Vercel routing configuration
├── .gitignore        # Git ignore file
└── README.md         # Project documentation and guide
```

---

## ☁️ Deploying to Vercel (Recommended & Error-Free)

Because standard Streamlit WebSocket processes are incompatible with Vercel's serverless timeouts, this project includes a dedicated **Vercel Serverless Entrypoint** (`api/index.py` + `vercel.json`) that serves the identical UI and AI knowledge engine with **zero timeouts, zero WebSocket drops, and instant response times**.

### Option A: Via GitHub (Simplest)
1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Add Vercel deployment support"
   git push origin main
   ```
2. Go to **[vercel.com/new](https://vercel.com/new)**.
3. Import your GitHub repository.
4. Leave all settings at default (Framework Preset: **Other**, Root Directory: `./`).
5. *(Optional)* Add Environment Variables for cloud models:
   - `GEMINI_API_KEY`: Your Google Gemini API Key
   - `OPENAI_API_KEY`: Your OpenAI API Key
6. Click **Deploy**. Vercel will build and deploy the app in seconds!

### Option B: Via Vercel CLI
Run from the root directory:
```bash
vercel
```

---

## 🚀 Getting Started Locally

### Prerequisites

Ensure you have Python 3.9+ installed, then install dependencies:

```bash
pip install -r requirements.txt
```

### Running with Streamlit
```bash
streamlit run chatbot.py
```
Opens in your browser at `http://localhost:8501`.

### Running with Vercel / Flask Serverless Runner Locally
```bash
python api/index.py
```
Opens in your browser at `http://localhost:3000`.

---

## ☁️ Deploying to Streamlit Community Cloud

1. **Push your repository to GitHub**:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
   - Click **"New app"**.
   - Select your repository, set the branch to `main`, and set **Main file path** to `chatbot.py`.
   - *(Optional)* In **Advanced settings > Secrets**, you can add your API keys:
     ```toml
     GEMINI_API_KEY = "your-gemini-key"
     OPENAI_API_KEY = "your-openai-key"
     ```
   - Click **"Deploy!"**.

---

## 📖 Offline Topics Reference

For a complete list of questions that the offline engine answers, refer to [`question.txt`](./question.txt).

