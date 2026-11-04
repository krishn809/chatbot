import os
import sys
import html
import json
import requests

AI_KNOWLEDGE = {
    "what_is_ai": {
        "title": "Artificial Intelligence (AI)",
        "keywords": ["what is ai", "define ai", "artificial intelligence", "intro to ai", "basics of ai", "explain ai"],
        "content": (
            "<b>Artificial Intelligence (AI)</b> refers to computer systems engineered to simulate human intelligence—such as "
            "learning from experience, reasoning, solving complex problems, and understanding natural language and vision.<br><br>"
            "🚗 <b>Analogy:</b> Traditional software is like a train on fixed railway tracks—it only moves where tracks are laid. "
            "AI is like an autonomous vehicle that reads unexpected road conditions, recalculates, and learns the optimal path.<br><br>"
            "<b>The 3 Stages of AI Development:</b><br>"
            "• <b>Narrow AI (ANI):</b> Specialized for specific tasks (ChatGPT, AlphaFold, Siri). This is current AI.<br>"
            "• <b>General AI (AGI):</b> Human-level cognitive adaptability across any intellectual domain.<br>"
            "• <b>Super AI (ASI):</b> Hypothetical intelligence surpassing collective human capability in scientific discovery and strategy."
        ),
        "quiz": "💡 <b>Quick Question:</b> Is an image recognition model for medical scans considered Narrow AI (ANI) or General AI (AGI)?"
    },
    "machine_learning": {
        "title": "Machine Learning (ML)",
        "keywords": ["machine learning", "what is ml", "how ml works", "learn ml", "types of ml"],
        "content": (
            "<b>Machine Learning</b> is the core branch of AI where algorithms discover patterns in historical data "
            "to make predictions or decisions without being explicitly hand-coded with rule logic.<br><br>"
            "🍳 <b>Analogy:</b> Traditional coding is following a strict recipe book. Machine Learning is a master chef "
            "tasting thousands of dishes and mathematically identifying the exact balance of flavors.<br><br>"
            "<b>The 3 Core Paradigms:</b><br>"
            "1. <b>Supervised Learning:</b> Training with labeled pairs (Input X ➔ Target Y). e.g., Spam detection, housing price regression.<br>"
            "2. <b>Unsupervised Learning:</b> Finding latent clusters in unlabeled data. e.g., Customer segmentation, anomaly detection.<br>"
            "3. <b>Reinforcement Learning:</b> Agents maximizing reward signals via trial and error. e.g., AlphaGo, autonomous driving."
        ),
        "quiz": "💡 <b>Quick Question:</b> If you train a model to forecast stock prices using historical price data, is that Supervised or Unsupervised?"
    },
    "deep_learning": {
        "title": "Deep Learning (DL)",
        "keywords": ["deep learning", "what is dl", "ann", "deep neural network"],
        "content": (
            "<b>Deep Learning</b> is a specialized subset of Machine Learning powered by multi-layered Artificial Neural Networks. "
            "The term 'deep' refers to having multiple hidden layers between the input and output.<br><br>"
            "👁️ <b>Analogy:</b> In facial recognition, Layer 1 detects simple edges; Layer 2 combines edges into curves and textures; "
            "Layer 3 forms eyes and noses; and final layers recognize the complete identity.<br><br>"
            "<b>Why Deep Learning exploded:</b><br>"
            "• <b>Automatic Feature Extraction:</b> Eliminates manual feature engineering.<br>"
            "• <b>Big Data & GPUs:</b> Massively parallel computation allows training on billions of parameters.<br>"
            "• <b>Versatility:</b> Powers speech recognition, self-driving vision, and generative art."
        ),
        "quiz": "💡 <b>Quick Question:</b> What makes Deep Learning different from traditional Machine Learning?"
    },
    "knn": {
        "title": "K-Nearest Neighbors (KNN)",
        "keywords": ["knn", "k-nearest neighbors", "k nearest neighbor", "knn algorithm"],
        "content": (
            "<b>K-Nearest Neighbors (KNN)</b> is a simple, intuitive, non-parametric Supervised Learning algorithm "
            "used for both <b>Classification</b> and <b>Regression</b>.<br><br>"
            "👥 <b>Analogy:</b> <i>'Birds of a feather flock together.'</i> If you want to know which political party someone supports, "
            "look at the 5 closest friends they hang out with—the majority party among those 5 is your prediction!<br><br>"
            "<b>How KNN Works:</b><br>"
            "1. Calculate mathematical distance (Euclidean, Manhattan) between a new data point and all training points.<br>"
            "2. Select the <b>K</b> closest neighbors.<br>"
            "3. For Classification: Take a majority vote. For Regression: Calculate the average value.<br><br>"
            "💡 <b>Tip:</b> If K is too small (e.g., K=1), the model is sensitive to noise (Overfitting). If K is too large, boundaries blur (Underfitting)."
        ),
        "quiz": "💡 <b>Quick Question:</b> Why is KNN called a 'Lazy Learner' algorithm?"
    },
    "neural_network": {
        "title": "Neural Networks (ANNs)",
        "keywords": ["neural network", "neural networks", "perceptron", "neurons", "layers", "backpropagation"],
        "content": (
            "An <b>Artificial Neural Network (ANN)</b> is a computing architecture inspired by biological neurons in the human brain.<br><br>"
            "🧠 <b>Key Anatomy:</b><br>"
            "• <b>Input Layer:</b> Receives numerical features (pixels, text tokens, tabular numbers).<br>"
            "• <b>Hidden Layers:</b> Nodes compute weighted sums: <code>z = \u2211(w\u1d62 \u00b7 x\u1d62) + b</code> and pass through activation functions.<br>"
            "• <b>Activation Functions:</b> Non-linear functions (ReLU, GELU, Sigmoid) enabling networks to learn complex curves.<br>"
            "• <b>Backpropagation & Gradient Descent:</b> Uses calculus chain rule to calculate prediction errors and update weights iteratively."
        ),
        "quiz": "💡 <b>Quick Question:</b> What is the purpose of the 'bias' (b) term in an artificial neuron?"
    },
    "turing_and_tuning": {
        "title": "Turing Test & Model Tuning",
        "keywords": ["tuning test", "turing test", "model tuning", "fine tuning", "hyperparameter tuning"],
        "content": (
            "This covers two essential AI concepts: <b>The Turing Test</b> and <b>Model Tuning</b>!<br><br>"
            "1️⃣ <b>The Turing Test (Alan Turing, 1950):</b><br>"
            "A test of a machine's ability to exhibit intelligent behavior indistinguishable from that of a human. "
            "If a human evaluator cannot reliably tell whether they are conversing with a human or a machine, the machine passes.<br><br>"
            "2️⃣ <b>Model Tuning & Fine-Tuning:</b><br>"
            "• <b>Hyperparameter Tuning:</b> Finding optimal learning rates, batch sizes, and tree depths (via Grid Search, Bayesian Optimization).<br>"
            "• <b>Fine-Tuning (LLMs):</b> Taking a pre-trained base model and training it further on domain-specific data (e.g., medical or legal texts)."
        ),
        "quiz": "💡 <b>Quick Question:</b> What is the difference between a model parameter (weights) and a hyperparameter (learning rate)?"
    },
    "history_of_ai": {
        "title": "History of Artificial Intelligence",
        "keywords": ["history of ai", "ai history", "timeline of ai", "when was ai founded"],
        "content": (
            "Artificial Intelligence has evolved over seven decades of breakthroughs and 'AI Winters':<br><br>"
            "• <b>1950 - The Spark:</b> Alan Turing publishes <i>'Computing Machinery and Intelligence'</i>, proposing the Turing Test.<br>"
            "• <b>1956 - The Birth:</b> The Dartmouth Summer Research Project officially coins the term 'Artificial Intelligence'.<br>"
            "• <b>1970s & 1980s - AI Winters:</b> Funding dried up when early symbolic systems failed to handle real-world messiness.<br>"
            "• <b>1997 - Deep Blue:</b> IBM's Deep Blue defeats World Chess Champion Garry Kasparov.<br>"
            "• <b>2012 - Deep Learning Era:</b> AlexNet wins ImageNet by a landslide using GPUs and CNNs.<br>"
            "• <b>2017 to Present - Generative AI:</b> Google introduces the Transformer architecture, sparking LLMs (ChatGPT, Gemini, Claude)."
        ),
        "quiz": "💡 <b>Quick Question:</b> What 1956 conference is considered the official birthplace of AI as a field?"
    },
    "founder_of_ai": {
        "title": "Founders and Pioneers of AI",
        "keywords": ["founder of ai", "father of ai", "who created ai", "who invented ai", "founders of ai"],
        "content": (
            "Several legendary visionaries earned the title of AI pioneers:<br><br>"
            "🏛️ <b>The Founding Fathers:</b><br>"
            "• <b>John McCarthy:</b> Known as the <i>'Father of AI'</i>. He coined the term 'Artificial Intelligence' in 1955 and created the LISP programming language.<br>"
            "• <b>Alan Turing:</b> The intellectual godfather who conceived machine intelligence and the Turing Test in 1950.<br>"
            "• <b>Marvin Minsky:</b> Co-founder of the MIT AI Laboratory, pioneering cognitive science, robotics, and early perceptrons.<br>"
            "• <b>Herbert Simon & Allen Newell:</b> Created the Logic Theorist (1956), widely called the first running AI program.<br><br>"
            "🌟 <b>Modern Deep Learning Godfathers:</b><br>"
            "• <b>Geoffrey Hinton, Yann LeCun, & Yoshua Bengio:</b> Won the 2018 Turing Award for pioneering modern Deep Learning."
        ),
        "quiz": "💡 <b>Quick Question:</b> Who coined the exact term 'Artificial Intelligence'?"
    },
    "how_ai_helps": {
        "title": "How AI Helps Humanity & Modern Society",
        "keywords": ["how ai helps", "benefits of ai", "why ai is useful", "ai applications", "how ai can help"],
        "content": (
            "Artificial Intelligence is transforming nearly every domain of human endeavor:<br><br>"
            "🩺 <b>Healthcare & Medicine:</b> Diagnosing cancers and retinal diseases earlier than human eye; AlphaFold solved 200M+ protein structures in days.<br>"
            "🌍 <b>Climate & Agriculture:</b> Optimizing renewable energy grids, predicting weather patterns, and guiding precision crop harvesting.<br>"
            "🚗 <b>Transportation:</b> Self-driving vehicles, logistics route optimization, and collision avoidance systems.<br>"
            "📚 <b>Education:</b> Personalized 24/7 AI tutoring adapted to each student's learning speed and style.<br>"
            "🔬 <b>Scientific Discovery:</b> Accelerating material discovery for clean batteries and simulating complex quantum systems."
        ),
        "quiz": "💡 <b>Quick Question:</b> In which field do you believe AI will have the largest positive impact over the next 10 years?"
    },
    "llms_transformers": {
        "title": "Large Language Models & Transformers",
        "keywords": ["llm", "large language model", "transformer", "chatgpt", "how do llms work", "attention mechanism", "self attention"],
        "content": (
            "<b>Large Language Models (LLMs)</b> are neural networks trained on vast text corpora to predict the most contextually relevant next token.<br><br>"
            "📚 <b>Analogy:</b> Imagine a researcher who has memorized every written book. When you write half a thought, "
            "they instantaneously predict the most cogent and insightful continuation.<br><br>"
            "<b>Key Building Blocks:</b><br>"
            "• <b>Tokenization:</b> Slicing raw text into token IDs.<br>"
            "• <b>Vector Embeddings:</b> Mapping words into continuous semantic vector spaces.<br>"
            "• <b>Self-Attention:</b> Dynamically calculating attention weights between all words in parallel."
        ),
        "quiz": "💡 <b>Quick Question:</b> What fundamental mechanism enables Transformers to process all words in a sentence in parallel?"
    }
}

def query_offline_tutor(user_prompt: str) -> str:
    prompt_clean = user_prompt.lower().strip()

    if prompt_clean in ["b", "k-means", "kmeans", "option b", "b)"]:
        return (
            "🎉 <b>Correct! Option B: K-Means Clustering!</b><br><br>"
            "Unlike Linear Regression, Random Forests, or SVMs (which require labeled ground-truth targets Y), "
            "<b>K-Means Clustering</b> groups unlabeled data points together based purely on spatial distance metrics.<br><br>"
            "🌟 <i>Great job! What AI concept would you like to explore next? (Check the sidebar for quick topics!)</i>"
        )
    elif prompt_clean in ["a", "c", "d", "option a", "option c", "option d"]:
        return (
            "❌ <b>Not quite! The correct answer is B: K-Means Clustering.</b><br><br>"
            "Linear Regression, Random Forests, and SVMs are all <b>Supervised Learning</b> algorithms that rely on labeled ground-truth pairs. "
            "K-Means uncovers clusters on unlabeled datasets without supervision!<br><br>"
            "💡 <i>Check the sidebar 'KNN' or 'Machine Learning' buttons to dive deeper!</i>"
        )

    best_match = None
    highest_score = 0
    for key, data in AI_KNOWLEDGE.items():
        score = 0
        for kw in data["keywords"]:
            if kw in prompt_clean:
                score += len(kw.split()) * 2
        if score > highest_score:
            highest_score = score
            best_match = data

    if best_match and highest_score > 0:
        return f"<b>{best_match['title']}</b><br><br>{best_match['content']}<br><br><hr>{best_match['quiz']}"

    safe_prompt = html.escape(user_prompt)
    return (
        f"<b>AI Insight: \"{safe_prompt}\"</b><br><br>"
        "Artificial Intelligence focuses on solving complex problems by extracting patterns from data rather than hardcoded logic.<br><br>"
        "<b>Core Pillars:</b><br>"
        "• <b>Data Tensors:</b> Encoding raw text, audio, and visual inputs into multi-dimensional matrices.<br>"
        "• <b>Neural Architecture:</b> Passing tensors through parameterized transformation layers (e.g., Attention, Convolutions).<br>"
        "• <b>Optimization:</b> Minimizing loss via Backpropagation and Gradient Descent.<br><br>"
        "💡 <b>Explore topics directly from the Sidebar:</b><br>"
        "• <i>AI, ML, DL, KNN, Neural Networks</i><br>"
        "• <i>History of AI & Founder of AI</i><br>"
        "• <i>Turing & Tuning Test, How AI Helps</i>"
    )

def generate_ai_response(prompt: str, api_choice: str, gemini_key: str, openai_key: str, selected_model: str) -> str:
    if api_choice == "Google Gemini" and gemini_key.strip():
        try:
            model = selected_model or "gemini-1.5-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key.strip()}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "systemInstruction": {
                    "parts": [{
                        "text": "You are an expert, friendly AI Tutor. Your role is to teach and explain Artificial Intelligence, Machine Learning, Deep Learning, and Data Science concepts clearly. Use simple language, intuitive analogies, concise bullet points, and end with an interactive question or quiz."
                    }]
                }
            }
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return html.escape(text).replace("\n", "<br>")
            else:
                return f"⚠️ <b>Gemini API Notice:</b> HTTP {res.status_code} - {html.escape(res.text[:200])}<br><br>" + query_offline_tutor(prompt)
        except Exception as e:
            return f"⚠️ <b>Gemini API Notice:</b> {html.escape(str(e))}<br><br>(Falling back to built-in engine below)<br><br>" + query_offline_tutor(prompt)

    elif api_choice == "OpenAI" and openai_key.strip():
        try:
            model = selected_model or "gpt-4o-mini"
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_key.strip()}"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an insightful AI Educator who explains AI concepts with clarity, real-world analogies, and interactive questions."},
                    {"role": "user", "content": prompt}
                ]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                text = data["choices"][0]["message"]["content"]
                return html.escape(text).replace("\n", "<br>")
            else:
                return f"⚠️ <b>OpenAI API Notice:</b> HTTP {res.status_code} - {html.escape(res.text[:200])}<br><br>" + query_offline_tutor(prompt)
        except Exception as e:
            return f"⚠️ <b>OpenAI API Notice:</b> {html.escape(str(e))}<br><br>(Falling back to built-in engine below)<br><br>" + query_offline_tutor(prompt)

    return query_offline_tutor(prompt)

