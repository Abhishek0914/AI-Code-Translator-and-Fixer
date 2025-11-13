# 💻 AI Code Translator & Error Fixer  
**Powered by Streamlit + Ollama + Open-Source LLMs**

> 🌍 Translate code between any two programming languages, fix syntax or runtime errors automatically, and visualize your results in a clean modern UI — all locally.

---

## 🚀 Overview

**AI Code Translator & Error Fixer** is an open-source tool that uses **Ollama-powered LLMs** (Phi-3, Llama-3.2, Mistral, etc.) to:
- Translate source code from one language to another.
- Automatically fix compilation or runtime errors.
- Provide minimal unified diffs for transparency.
- Run fully offline with local models.

It’s built using **Streamlit** for the frontend and integrates directly with your **local Ollama API**.

---

## 🧠 Features

✅ Translate between any two programming languages (e.g., Python → Rust, Java → Go)  
✅ Fix syntax and runtime errors automatically  
✅ Show minimal diffs between original and corrected code  
✅ Detect common issues like missing brackets or mismatched parentheses  
✅ Beautiful dual-column Streamlit UI (Light & Dark themes)  
✅ Works offline — no OpenAI API required  
✅ Built entirely with open-source components  

---

## 🖼️ App Preview

### 🔹 Main Interface  
![App UI](assets/ui_screenshot.png)

> Left: Source code input + translation controls  
> Right: Translated code display  
> Bottom: Error correction section  

---

## ⚙️ Tech Stack

| Component | Description |
|------------|-------------|
| **Frontend** | Streamlit (Custom CSS, Light/Dark theme) |
| **Backend** | Python + Ollama API |
| **Models Supported** | Phi-3 Mini, Llama-3.2, Mistral, CodeLlama |
| **Error Detection** | Bracket/Parenthesis checker |
| **Version Control** | Git + GitHub |
| **Deployment** | Localhost, Streamlit Cloud, or AWS EC2 |

---

## 🧩 Setup Instructions


### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Abhishek0914/AI-Code-Translator-and-Fixer.git
cd AI-Code-Translator-and-Fixer

### 2️⃣ Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Mac/Linux
# OR
.\.venv\Scripts\activate   # On Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Run Ollama
ollama pull phi3:mini

### 5️⃣ Launch the App
streamlit run app.py
then visit http://localhost:8501

###🧠 How It Works

1. User enters source code + target language.

2. Code is sent to the Ollama model using requests.

3. Model translates the logic and syntax faithfully.

4. Users can paste errors; the system prompts the LLM to self-correct.

5. Optional unified diffs show exactly what changed.

### 🧑‍💻 For Developers

- To extend functionality:

- Add new prompt templates for optimization, security scan, or refactoring.

- Integrate real-time syntax validation with ast or esprima.

- Replace the Ollama model dynamically from the Streamlit dropdown.