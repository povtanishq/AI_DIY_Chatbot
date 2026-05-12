import streamlit as st
from google import genai  # Note the change: from google import genai

# ─────────────────────────────────────────────
#  Gemini API setup (The 2026 Way)
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  Gemini API setup (Strict & Detailed)
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful AI DIY home improvement assistant. 

CORE BEHAVIOR:
1. GREETINGS: You may respond normally to simple greetings like "Hi", "Hello", or "How are you?".
2. REPAIR QUESTIONS: When asked how to fix something, you MUST provide the answer immediately in this structure:
   - **Required Tools** (List them)
   - **Step-by-Step Instructions** (Numbered list)
3. NON-DIY TOPICS: If the user asks about something totally unrelated to home repair (like geography, math, or history), only then say: "I'm sorry, but I can only help with DIY and home improvement-related questions."
4. NO FLUFF: Skip introductory sentences like "Fixing this is easy." Get straight to the steps.
5. SAFETY: Always put a bold ⚠️ SAFETY WARNING at the start if the task involves water, electricity, or tools."""

# Initialize client
client = genai.Client(api_key="AIzaSyCZLZR9nSM7L7ktUUqVWoV_uIQvpLSBhuU")

def get_gemini_response(messages: list) -> str:
    try:
        user_msg = messages[-1]['content']
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=user_msg,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.3,
                "max_output_tokens": 1200 # Increased to allow for full steps
            }
        )
        return response.text

    except Exception as e:
        return f"Something went wrong: {e}"
# ─────────────────────────────────────────────
#  The rest of your Streamlit UI code remains 
#  largely the same, just ensure you call 
#  get_gemini_response(st.session_state.messages)
# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
#  Page config & CSS
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI DIY Assistant", page_icon="🛠️", layout="wide")

st.markdown("""
<style>
header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { visibility: hidden !important; }

body { background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%); }

.block-container { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }

h1 {
    color: #e5e7eb !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 0.4rem !important;
}

h3 {
    color: #9ca3af !important;
    font-size: 1.2rem !important;
    font-weight: 400 !important;
    text-align: center;
    margin-bottom: 2.5rem !important;
}

.toolkit-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    margin-bottom: 2.5rem;
}

.toolkit-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 18px;
    padding: 1.6rem 1rem;
    text-align: center;
    transition: all 0.25s ease;
    backdrop-filter: blur(10px);
}

.toolkit-card:hover {
    transform: translateY(-6px);
    border-color: #6366f1;
    box-shadow: 0 16px 32px rgba(99, 102, 241, 0.15);
}

.toolkit-icon { font-size: 2rem; display: block; margin-bottom: 0.6rem; }
.toolkit-title { font-size: 1rem; font-weight: 600; color: #e5e7eb; margin-bottom: 0.3rem; }
.toolkit-desc  { font-size: 0.8rem; color: #9ca3af; }

.chat-box {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2rem;
    max-width: 720px;
    margin: 0 auto 1.5rem auto;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
}

[data-testid="stChatMessageContent"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    color: #e5e7eb !important;
}

[data-testid="stChatInput"] textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #e5e7eb !important;
    font-size: 1rem !important;
    /* This removes the red/blue focus line */
    outline: none !important;
    box-shadow: none !important;
}

/* Forces the line to stay away when you click it */
[data-testid="stChatInput"] textarea:focus {
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid #6366f1 !important; /* Optional: adds a soft purple border instead */
}

/* Removes the red border from the parent container */
[data-testid="stChatInput"] {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.display_msgs = [
        {"role": "assistant", "content": "Hi! I'm your DIY assistant. Ask me anything about home repairs — plumbing, electrical, woodwork, painting, and more. 🛠️"}
    ]


# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
st.title("🛠️ AI DIY Home Improvement Guide")
st.markdown("### 🧰 DIY Toolkit")

st.markdown("""
<div class="toolkit-grid">
    <div class="toolkit-card">
        <span class="toolkit-icon">🔧</span>
        <div class="toolkit-title">Plumbing</div>
        <div class="toolkit-desc">Fix leaks, taps, pipes</div>
    </div>
    <div class="toolkit-card">
        <span class="toolkit-icon">🔌</span>
        <div class="toolkit-title">Electrical</div>
        <div class="toolkit-desc">Switches, wiring basics</div>
    </div>
    <div class="toolkit-card">
        <span class="toolkit-icon">🪚</span>
        <div class="toolkit-title">Woodwork</div>
        <div class="toolkit-desc">Furniture & repairs</div>
    </div>
    <div class="toolkit-card">
        <span class="toolkit-icon">🧰</span>
        <div class="toolkit-title">Tools</div>
        <div class="toolkit-desc">Usage & guidance</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("**Fix things like a pro without calling one 😎**")

st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.display_msgs:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your DIY question...")

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Handle new message
# ─────────────────────────────────────────────
if user_input:
    st.session_state.display_msgs.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Thinking…"):
            reply = get_gemini_response(st.session_state.messages)
        st.markdown(reply)

    st.session_state.display_msgs.append({"role": "assistant", "content": reply})
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()