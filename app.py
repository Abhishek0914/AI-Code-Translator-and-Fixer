import streamlit as st
import requests
import time

OLLAMA_API_URL = "http://localhost:11434/api/generate"

TRANSLATION_PROMPT = """
You are an expert multilingual code translator.
Translate the following {source_lang} code into {target_lang}.
Preserve the logic, structure, and comments.
Do not add explanations or extra text.
Respond with only the translated {target_lang} code.

Source ({source_lang}) Code:
{code}
"""

ERROR_FIX_PROMPT = """
You are an expert software engineer and strict code repair assistant.

TASK:
Fix the provided {lang} code so it runs without syntax or compilation errors.

RESPONSE RULES:
- Output ONLY the fully corrected code. No extra words, no explanations, no code fences.
- Maintain the original indentation, variable names, and logic.
- Do NOT insert placeholder lines like 'intermediate result' or comments that were not in the original.
- If you make changes, ensure the code is syntactically valid and logically identical.
- After the corrected code, output a minimal unified diff showing only your edits, starting with a new line containing:
===DIFF===
If you cannot confidently fix the code, respond with:
CANNOT_FIX: [short reason]

INPUT:
Language: {lang}
Original Code:
{code}

Compiler / Runtime Errors:
{errors}
"""

def check_bracket_balance(code: str):
    pairs = {"(": ")", "{": "}", "[": "]"}
    opens = []
    issues = []
    for i, ch in enumerate(code):
        if ch in pairs:
            opens.append((ch, i))
        elif ch in pairs.values():
            if not opens:
                issues.append(f"Unmatched closing '{ch}' at position {i}")
            else:
                last_open, _ = opens[-1]
                if pairs[last_open] == ch:
                    opens.pop()
                else:
                    issues.append(f"Mismatched '{last_open}' and '{ch}' at position {idx}")
    for o, idx in opens:
        issues.append(f"Unclosed '{o}' starting at position {idx}")
    return issues

def generate_response(prompt, model):
    """Send prompt to Ollama API and return model response."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "⚠️ No response received.")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {e}"

def translate_code(code, source_lang, target_lang, model):
    prompt = TRANSLATION_PROMPT.format(source_lang=source_lang, target_lang=target_lang, code=code)
    return generate_response(prompt, model)

def fix_code_errors(code, lang, errors, model, max_attempts=3):
    """Attempt to fix code iteratively and check for basic syntax issues."""
    current_code = code
    bracket_issues = check_bracket_balance(current_code)
    if bracket_issues:
        errors += "\nDetected possible bracket/parenthesis issues: " + "; ".join(bracket_issues)

    for attempt in range(max_attempts):
        prompt = ERROR_FIX_PROMPT.format(lang=lang, code=current_code, errors=errors)
        response = generate_response(prompt, model).strip()

        # If model returns same code again, retry with stronger hint
        if response.strip() == current_code.strip():
            errors += "\n⚠️ The last fix attempt didn't change the code. Try harder to fix syntax and structure issues."
            time.sleep(1)
            continue

        # Recheck bracket balance on new code
        bracket_issues = check_bracket_balance(response)
        if not bracket_issues:
            return response
        else:
            errors += "\nStill found bracket issues: " + "; ".join(bracket_issues)
            current_code = response
            time.sleep(1)

    return "⚠️ Model could not fully fix the code after several attempts.\nLast Attempt:\n\n" + response


st.set_page_config(page_title="AI Code Translator + Fixer", page_icon="💻", layout="wide")

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb, #90caf9);
            transition: background 0.8s ease-in-out;
        }

        @media (prefers-color-scheme: dark) {
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0a192f, #112240, #1b263b);
            }
            .main-title { color: #64b5f6 !important; }
            .subtitle { color: #90caf9 !important; }
            .section { background-color: rgba(255,255,255,0.06) !important; }
            .stTextArea textarea, .stTextInput input {
                background-color: rgba(255,255,255,0.05);
                color: #e3f2fd;
                border: 1px solid #64b5f6;
            }
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.2em;
            margin-top: 0;
            color: #0d47a1;
            animation: fadeIn 1.2s ease;
        }

        .subtitle {
            text-align: center;
            color: #1976d2;
            font-size: 1.05rem;
            margin-bottom: 1.5em;
            margin-top: 0;
            letter-spacing: 0.3px;
            animation: fadeIn 1.8s ease;
        }

        .section {
            background-color: rgba(255, 255, 255, 0.75);
            border-radius: 15px;
            padding: 1.7em;
            margin-bottom: 1em;
            margin-top: 0;
            box-shadow: 0 4px 14px rgba(0,0,0,0.1);
            backdrop-filter: blur(6px);
            animation: fadeIn 1.5s ease;
            transition: 0.3s ease-in-out;
        }

        .section:hover {
            box-shadow: 0 8px 20px rgba(30,136,229,0.25);
            transform: translateY(-2px);
        }

        .stTextArea textarea, .stTextInput input {
            border-radius: 10px;
            border: 1px solid #64b5f6;
        }

        .stButton button {
            background: linear-gradient(90deg, #1976d2, #42a5f5);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 0px rgba(33,150,243,0.0);
        }

        .stButton button:hover {
            background: linear-gradient(90deg, #1565c0, #1e88e5);
            transform: scale(1.04);
            box-shadow: 0 0 12px rgba(30,136,229,0.6);
        }

        .stCodeBlock {
            border-radius: 10px !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        p.footer {
            text-align: center;
            color: gray;
            margin-top: 2em;
            font-size: 0.9rem;
        }
        
        /* Reduce default Streamlit spacing */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        div[data-testid="column"] {
            padding: 0 !important;
        }
        
        .element-container {
            margin-bottom: 0.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">AI Code Translator & Error Fixer</div>
<div class="subtitle">Translate and debug your code seamlessly — powered by open-source LLMs.</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# --- Left Column: Translation ---
with col1:
    
    st.subheader("Source Code")
    code_input = st.text_area("Paste your code here:", height=300, placeholder="Enter your source code...")
    
    col1a, col1b = st.columns(2)
    with col1a:
        source_lang = st.text_input("Source Language:", "Python")
    with col1b:
        target_lang = st.text_input("Target Language:", "Rust")

    model_choice = st.selectbox("Choose Model:", ["phi3:mini", "llama3.2", "mistral", "codellama"])
    translate_button = st.button("Translate Code")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Right Column: Output ---
with col2:
    
    st.subheader("Translated Code")
    translated_code = ""
    if translate_button:
        with st.spinner(f"Translating {source_lang} → {target_lang}..."):
            translated_code = translate_code(code_input, source_lang, target_lang, model_choice)
            st.code(translated_code, language=target_lang.lower())
    st.markdown('</div>', unsafe_allow_html=True)

# --- Error Fix Section ---
st.subheader("Error Correction")

error_code_input = st.text_area("Paste the code that produced errors:", height=200, placeholder="Paste your code here...")
error_text_input = st.text_area("Paste the error message here:", height=150, placeholder="Copy-paste your compiler or runtime errors here...")
error_lang = st.text_input("Language of the code:", "Rust")

fix_button = st.button("Fix My Code")

if fix_button:
    with st.spinner("Analyzing and correcting errors..."):
        fixed_code = fix_code_errors(error_code_input, error_lang, error_text_input, model_choice)
        st.subheader("Corrected Code")
        st.code(fixed_code, language=error_lang.lower())
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p class='footer'>Built with Streamlit + Ollama | Designed by AbhisheksHyper</p>", unsafe_allow_html=True)
