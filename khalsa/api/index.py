import os
import sys
import html
from flask import Flask, request, jsonify, render_template_string

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ai_engine import query_offline_tutor, generate_ai_response, AI_KNOWLEDGE

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot | Minimalist AI Tutor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background: 
                radial-gradient(circle at 10% 12%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 88%, rgba(52, 211, 153, 0.08) 0%, transparent 40%),
                #f8fafc;
            color: #1e293b;
            min-height: 100vh;
            display: flex;
            position: relative;
            overflow-x: hidden;
        }

        /* Top-Left Black Sidebar Toggle */
        .sidebar-toggle-btn {
            position: fixed;
            top: 14px;
            left: 14px;
            z-index: 1000;
            background: #ffffff;
            color: #000000;
            border: 2px solid #000000;
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 1.1rem;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .sidebar-toggle-btn:hover {
            background: #000000;
            color: #ffffff;
        }

        /* Sidebar */
        .sidebar {
            width: 310px;
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
            padding: 60px 18px 24px 18px;
            height: 100vh;
            overflow-y: auto;
            position: fixed;
            left: 0;
            top: 0;
            z-index: 900;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 2px 0 15px rgba(0, 0, 0, 0.03);
        }

        .sidebar.collapsed {
            transform: translateX(-100%);
        }

        .sidebar-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .sidebar-label {
            font-size: 0.76rem;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin: 14px 0 6px 0;
            display: block;
        }

        .sidebar select, .sidebar input[type="text"], .sidebar input[type="password"] {
            width: 100%;
            padding: 8px 12px;
            border-radius: 10px;
            border: 1px solid #cbd5e1;
            font-size: 0.88rem;
            color: #000000;
            background: #ffffff;
            margin-bottom: 8px;
            outline: none;
            transition: border-color 0.2s ease;
        }

        .sidebar select:focus, .sidebar input:focus {
            border-color: #0ea5e9;
        }

        .sidebar hr {
            border: none;
            border-top: 1px solid #f1f5f9;
            margin: 16px 0;
        }

        /* Rewards Box */
        .rewards-box {
            background: linear-gradient(135deg, #f0f9ff 0%, #ecfdf5 100%);
            border: 1px solid #bae6fd;
            border-radius: 16px;
            padding: 14px;
            text-align: center;
            margin-bottom: 14px;
        }

        .reward-title {
            font-size: 0.74rem;
            text-transform: uppercase;
            font-weight: 800;
            color: #0369a1;
            letter-spacing: 0.8px;
        }

        .reward-points {
            font-size: 1.5rem;
            font-weight: 800;
            color: #0f172a;
            margin: 4px 0;
        }

        .badge-pill {
            display: inline-block;
            background: #ffffff;
            border: 1px solid #a7f3d0;
            color: #059669;
            font-weight: 700;
            font-size: 0.78rem;
            padding: 2px 10px;
            border-radius: 999px;
            box-shadow: 0 2px 6px rgba(16, 185, 129, 0.1);
        }

        .progress-bar-bg {
            background: #e2e8f0;
            height: 6px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }

        .progress-bar-fill {
            background: linear-gradient(90deg, #0ea5e9, #10b981);
            height: 100%;
            width: 0%;
            transition: width 0.3s ease;
        }

        /* Quiz Box */
        .quiz-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 12px;
        }

        .quiz-question {
            font-size: 0.84rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
        }

        .quiz-option {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.82rem;
            color: #334155;
            margin-bottom: 6px;
            cursor: pointer;
        }

        .quiz-btn {
            background: #0ea5e9;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 0.8rem;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            margin-top: 6px;
        }

        .quiz-msg {
            font-size: 0.8rem;
            margin-top: 8px;
            font-weight: 600;
            display: none;
        }

        /* Short Question Buttons */
        .short-q-btn {
            background: #ffffff;
            color: #0f172a;
            border: 1px solid #e0f2fe;
            border-radius: 10px;
            padding: 7px 10px;
            font-size: 0.82rem;
            font-weight: 600;
            width: 100%;
            margin-bottom: 6px;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s ease;
        }

        .short-q-btn:hover {
            background: #f0f9ff;
            color: #0284c7;
            border-color: #38bdf8;
            transform: translateY(-1px);
        }

        /* Main Content Container */
        .main-content {
            flex: 1;
            margin-left: 310px;
            display: flex;
            justify-content: center;
            padding: 24px 16px;
            transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .main-content.expanded {
            margin-left: 0;
        }

        .chat-card {
            max-width: 680px;
            width: 100%;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 24px;
            box-shadow: 0 12px 35px rgba(14, 165, 233, 0.05), 0 2px 8px rgba(0, 0, 0, 0.02);
            padding: 24px 28px;
            display: flex;
            flex-direction: column;
            min-height: 600px;
            position: relative;
        }

        /* Minimal Header */
        .minimal-header {
            text-align: center;
            padding: 4px 0 14px 0;
            border-bottom: 1px solid #f1f5f9;
            margin-bottom: 16px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #059669;
            font-size: 0.76rem;
            font-weight: 700;
            padding: 3px 12px;
            border-radius: 999px;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
            display: inline-block;
            animation: pulse-green 2s infinite ease-in-out;
        }

        @keyframes pulse-green {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        .minimal-title {
            font-size: 1.9rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.5px;
            margin: 2px 0 4px 0;
        }

        .minimal-title span {
            background: linear-gradient(135deg, #0284c7 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .minimal-subtitle {
            color: #64748b;
            font-size: 0.92rem;
            font-weight: 400;
            margin: 0;
        }

        /* Featured Topics Grid */
        .featured-topics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 14px 0 20px 0;
        }

        .topic-pill-btn {
            background: #ffffff;
            color: #0f172a;
            border: 1px solid #e0f2fe;
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 0.86rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.04);
            transition: all 0.2s ease;
            text-align: center;
        }

        .topic-pill-btn:hover {
            background: #f0f9ff;
            color: #0284c7;
            border-color: #38bdf8;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.14);
            transform: translateY(-1.5px);
        }

        /* Chat Scroll Area */
        .chat-scroll-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-bottom: 18px;
            max-height: 440px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .chat-scroll-area::-webkit-scrollbar {
            width: 5px;
        }
        .chat-scroll-area::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 8px;
        }
        .chat-scroll-area::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 8px;
        }
        .chat-scroll-area::-webkit-scrollbar-thumb:hover {
            background: #38bdf8;
        }

        .bubble-user {
            align-self: flex-end;
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            color: #0369a1;
            padding: 11px 16px;
            border-radius: 18px 18px 4px 18px;
            max-width: 82%;
            font-size: 0.93rem;
            line-height: 1.5;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.04);
            margin-left: auto;
            word-break: break-word;
            font-weight: 500;
        }

        .bubble-bot {
            align-self: flex-start;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 3.5px solid #10b981;
            color: #1e293b;
            padding: 16px 20px;
            border-radius: 4px 18px 18px 18px;
            max-width: 92%;
            font-size: 0.92rem;
            line-height: 1.62;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03);
            word-break: break-word;
        }

        .bot-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            color: #059669;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            padding: 2px 8px;
            border-radius: 6px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .bubble-bot b, .bubble-bot strong {
            color: #0f172a;
        }

        .bubble-bot hr {
            border: none;
            border-top: 1px solid #f1f5f9;
            margin: 12px 0;
        }

        /* Typing Space */
        .typing-form {
            display: flex;
            align-items: center;
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 18px;
            padding: 6px 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
            transition: all 0.2s ease;
        }

        .typing-form:focus-within {
            border-color: #0ea5e9;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12), 0 4px 16px rgba(14, 165, 233, 0.08);
        }

        .typing-input {
            flex: 1;
            border: none;
            outline: none;
            background: transparent;
            color: #000000;
            font-size: 0.96rem;
            padding: 8px 12px;
            font-weight: 500;
            caret-color: #0ea5e9;
        }

        .typing-input::placeholder {
            color: #94a3b8;
            font-weight: 400;
        }

        .send-btn {
            background: linear-gradient(135deg, #0ea5e9 0%, #10b981 100%);
            color: #ffffff;
            border: none;
            border-radius: 12px;
            height: 42px;
            width: 44px;
            font-size: 1.2rem;
            font-weight: 800;
            box-shadow: 0 2px 10px rgba(14, 165, 233, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
        }

        .clear-chat-btn {
            background: transparent;
            color: #64748b;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            margin: 8px auto 0 auto;
            display: block;
            transition: all 0.2s ease;
        }

        .clear-chat-btn:hover {
            color: #0f172a;
            border-color: #94a3b8;
        }

        @media (max-width: 800px) {
            .sidebar {
                transform: translateX(-100%);
            }
            .sidebar.active-mobile {
                transform: translateX(0);
            }
            .main-content {
                margin-left: 0;
            }
            .featured-topics {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

    <!-- Top Left Black Sidebar Toggle Button -->
    <button class="sidebar-toggle-btn" id="sidebarToggleBtn" title="Toggle Sidebar">☰</button>

    <!-- Sidebar -->
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-title">⚙️ AI Engine & Keys</div>

        <label class="sidebar-label">Intelligence Provider</label>
        <select id="engineSelect">
            <option value="Built-in AI Tutor (Offline & Free)">Built-in AI Tutor (Offline & Free)</option>
            <option value="Google Gemini">Google Gemini</option>
            <option value="OpenAI">OpenAI</option>
        </select>

        <div id="geminiConfig" style="display: none;">
            <label class="sidebar-label">Gemini API Key</label>
            <input type="password" id="geminiKey" placeholder="Enter Gemini API Key">
            <label class="sidebar-label">Model</label>
            <select id="geminiModel">
                <option value="gemini-1.5-flash">gemini-1.5-flash</option>
                <option value="gemini-1.5-pro">gemini-1.5-pro</option>
                <option value="gemini-2.0-flash">gemini-2.0-flash</option>
            </select>
        </div>

        <div id="openaiConfig" style="display: none;">
            <label class="sidebar-label">OpenAI API Key</label>
            <input type="password" id="openaiKey" placeholder="Enter OpenAI API Key">
            <label class="sidebar-label">Model</label>
            <select id="openaiModel">
                <option value="gpt-4o-mini">gpt-4o-mini</option>
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
            </select>
        </div>

        <hr>

        <!-- Rewards Tracker -->
        <label class="sidebar-label">🏆 Learning Rewards</label>
        <div class="rewards-box">
            <div class="reward-title">Total XP Earned</div>
            <div class="reward-points" id="xpDisplay">0 XP</div>
            <div class="badge-pill" id="badgeDisplay">🌱 AI Novice</div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="xpProgressBar"></div>
            </div>
        </div>

        <!-- Quick AI Quiz -->
        <label class="sidebar-label">🎯 Quick AI Quiz</label>
        <div class="quiz-card">
            <div class="quiz-question">Which of the following is an Unsupervised Learning algorithm?</div>
            <label class="quiz-option"><input type="radio" name="quiz_opt" value="Linear Regression"> Linear Regression</label>
            <label class="quiz-option"><input type="radio" name="quiz_opt" value="K-Means Clustering"> K-Means Clustering</label>
            <label class="quiz-option"><input type="radio" name="quiz_opt" value="Random Forest Classifier"> Random Forest Classifier</label>
            <label class="quiz-option"><input type="radio" name="quiz_opt" value="Support Vector Machines"> Support Vector Machines</label>
            <button class="quiz-btn" id="checkQuizBtn">Check Answer (+15 XP)</button>
            <div class="quiz-msg" id="quizFeedback"></div>
        </div>

        <hr>

        <!-- Short Questions Library -->
        <label class="sidebar-label">📚 Short AI Questions (+5 XP)</label>
        <button class="short-q-btn" data-query="What is Artificial Intelligence and how does it work?">🤖 What is AI?</button>
        <button class="short-q-btn" data-query="Explain Machine Learning and its 3 main types.">🍳 What is ML?</button>
        <button class="short-q-btn" data-query="What is Deep Learning and how does it differ from ML?">👁️ What is DL?</button>
        <button class="short-q-btn" data-query="Explain the K-Nearest Neighbors (KNN) algorithm with an analogy.">👥 What is KNN?</button>
        <button class="short-q-btn" data-query="How do Artificial Neural Networks learn with backpropagation?">🧠 Neural Network</button>
        <button class="short-q-btn" data-query="Explain the Turing Test and Model Hyperparameter Tuning.">🧪 Turing & Tuning Test</button>
        <button class="short-q-btn" data-query="What is the history and timeline of Artificial Intelligence?">📜 History of AI</button>
        <button class="short-q-btn" data-query="Who is the founder and pioneers of Artificial Intelligence?">🏛️ Founder of AI</button>
        <button class="short-q-btn" data-query="How does AI help humanity in healthcare, climate, and daily life?">🩺 How AI Helps</button>
    </aside>

    <!-- Main Content -->
    <main class="main-content" id="mainContent">
        <div class="chat-card">
            <div class="minimal-header">
                <div class="status-badge">
                    <span class="status-dot"></span> AI Learning Hub Active
                </div>
                <div class="minimal-title">AI Intelligence <span>Hub</span></div>
                <p class="minimal-subtitle">Ask anything about Machine Learning, Neural Networks & Generative AI</p>
            </div>

            <!-- Featured Topics (Hidden when chat starts) -->
            <div class="featured-topics" id="featuredTopics">
                <button class="topic-pill-btn" data-query="What is Machine Learning and what are its main types?">🧠 Machine Learning</button>
                <button class="topic-pill-btn" data-query="Explain Deep Learning and how artificial neural networks learn.">⚡ Neural Networks</button>
                <button class="topic-pill-btn" data-query="Explain K-Nearest Neighbors (KNN) algorithm with an analogy.">👥 KNN Algorithm</button>
                <button class="topic-pill-btn" data-query="Who is the founder of Artificial Intelligence and who are its pioneers?">🏛️ Founders of AI</button>
                <button class="topic-pill-btn" data-query="How does AI help humanity in healthcare, climate, and daily life?">🩺 How AI Helps</button>
                <button class="topic-pill-btn" data-query="How do Large Language Models and Transformers work?">🎯 Transformers & LLMs</button>
            </div>

            <!-- Chat Scroll Area -->
            <div class="chat-scroll-area" id="chatArea"></div>

            <!-- Typing Space -->
            <form class="typing-form" id="chatForm">
                <input type="text" class="typing-input" id="userInput" placeholder="Ask any question about AI, ML, DL, KNN, History..." autocomplete="off">
                <button type="submit" class="send-btn" title="Send Question">➔</button>
            </form>
            <button class="clear-chat-btn" id="clearChatBtn" style="display: none;">🔄 New Conversation</button>
        </div>
    </main>

    <script>
        let currentXP = 0;
        let quizDone = false;

        function updateXP(points) {
            currentXP += points;
            document.getElementById('xpDisplay').innerText = currentXP + ' XP';
            
            let badge = '🌱 AI Novice';
            if (currentXP >= 100) badge = '🏆 AI Grandmaster';
            else if (currentXP >= 60) badge = '⚡ Neural Architect';
            else if (currentXP >= 30) badge = '🧠 Deep Explorer';
            
            document.getElementById('badgeDisplay').innerText = badge;
            const progress = Math.min((currentXP / 100) * 100, 100);
            document.getElementById('xpProgressBar').style.width = progress + '%';
        }

        // Sidebar Collapse/Expand Toggle
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('mainContent');
        const toggleBtn = document.getElementById('sidebarToggleBtn');

        toggleBtn.addEventListener('click', () => {
            if (window.innerWidth <= 800) {
                sidebar.classList.toggle('active-mobile');
            } else {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('expanded');
            }
        });

        // Engine Select Toggle
        const engineSelect = document.getElementById('engineSelect');
        const geminiConfig = document.getElementById('geminiConfig');
        const openaiConfig = document.getElementById('openaiConfig');

        engineSelect.addEventListener('change', () => {
            geminiConfig.style.display = engineSelect.value === 'Google Gemini' ? 'block' : 'none';
            openaiConfig.style.display = engineSelect.value === 'OpenAI' ? 'block' : 'none';
        });

        // Chat Form Submission
        const chatForm = document.getElementById('chatForm');
        const userInput = document.getElementById('userInput');
        const chatArea = document.getElementById('chatArea');
        const featuredTopics = document.getElementById('featuredTopics');
        const clearChatBtn = document.getElementById('clearChatBtn');

        function appendMessage(role, text) {
            featuredTopics.style.display = 'none';
            clearChatBtn.style.display = 'block';

            const div = document.createElement('div');
            if (role === 'user') {
                div.className = 'bubble-user';
                div.innerText = text;
            } else {
                div.className = 'bubble-bot';
                div.innerHTML = '<span class="bot-badge">● AI TUTOR</span><div>' + text + '</div>';
            }
            chatArea.appendChild(div);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        async function sendQuery(queryText) {
            if (!queryText.trim()) return;
            appendMessage('user', queryText);
            userInput.value = '';

            const payload = {
                message: queryText,
                engine: engineSelect.value,
                gemini_key: document.getElementById('geminiKey').value,
                gemini_model: document.getElementById('geminiModel').value,
                openai_key: document.getElementById('openaiKey').value,
                openai_model: document.getElementById('openaiModel').value
            };

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                appendMessage('bot', data.reply);
                updateXP(5);
            } catch (err) {
                appendMessage('bot', '⚠️ Error contacting AI Tutor. Please check network connection.');
            }
        }

        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            sendQuery(userInput.value);
        });

        // Quick Topic & Short Question Clicks
        document.querySelectorAll('[data-query]').forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.getAttribute('data-query');
                sendQuery(query);
            });
        });

        // Clear Chat
        clearChatBtn.addEventListener('click', () => {
            chatArea.innerHTML = '';
            featuredTopics.style.display = 'grid';
            clearChatBtn.style.display = 'none';
        });

        // Quiz Submit
        const checkQuizBtn = document.getElementById('checkQuizBtn');
        const quizFeedback = document.getElementById('quizFeedback');

        checkQuizBtn.addEventListener('click', () => {
            const selected = document.querySelector('input[name="quiz_opt"]:checked');
            if (!selected) {
                quizFeedback.style.display = 'block';
                quizFeedback.style.color = '#eab308';
                quizFeedback.innerText = 'Please select an option first.';
                return;
            }
            if (selected.value === 'K-Means Clustering') {
                quizFeedback.style.display = 'block';
                quizFeedback.style.color = '#059669';
                quizFeedback.innerText = '🎉 Correct! K-Means discovers clusters without labels. +15 XP!';
                if (!quizDone) {
                    updateXP(15);
                    quizDone = true;
                }
            } else {
                quizFeedback.style.display = 'block';
                quizFeedback.style.color = '#ef4444';
                quizFeedback.innerText = '❌ Not quite! K-Means Clustering is unsupervised.';
            }
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "").strip()
    engine = data.get("engine", "Built-in AI Tutor (Offline & Free)")
    gemini_key = data.get("gemini_key", "").strip()
    openai_key = data.get("openai_key", "").strip()
    selected_model = data.get("gemini_model") or data.get("openai_model") or ""

    if not message:
        return jsonify({"reply": "Please type a question about AI to begin!"})

    reply = generate_ai_response(message, engine, gemini_key, openai_key, selected_model)
    return jsonify({"reply": reply, "xp": 5})

if __name__ == "__main__":
    app.run(debug=True, port=3000)

