import streamlit as st
import requests
import os

# 🔑 Gemini function
def get_gemini_response(user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={os.getenv('GEMINI_API_KEY')}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
You are a helpful AI assistant specialized in giving clear, step-by-step, practical answers.

User question: {user_input}

Give a direct, useful, real-world answer. Avoid generic suggestions.
"""
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", None)

    except:
        return None

# 🛠️ Fallback
def fallback_response(user_input):
    user_input = user_input.lower()

    if "tap" in user_input or "leak" in user_input:
        return """Fix a leaking tap:
1. Turn off water supply
2. Remove handle
3. Replace washer
4. Reassemble
5. Turn water on"""

    elif "paint" in user_input or "wall" in user_input:
        return """Paint a wall:
1. Clean the surface
2. Apply primer
3. Paint evenly
4. Let it dry
5. Apply second coat"""

    elif "switch" in user_input or "electric" in user_input:
        return """Fix a switch:
1. Turn off main power
2. Remove switch cover
3. Check wiring
4. Replace faulty switch
5. Turn power back on"""

    elif "drain" in user_input or "block" in user_input:
        return """Unblock a drain:
1. Pour hot water
2. Use plunger
3. Use baking soda + vinegar
4. Clean pipe
5. Test flow"""

    else:
        return """I can help with:
• Plumbing (tap, leaks)
• Painting
• Electrical (switch, wiring)
• Drain issues

Try asking clearly like:
"How to fix a leaking tap?" """

# 🎨 PAGE CONFIG
st.set_page_config(page_title="AI DIY Assistant", page_icon="🛠️", layout="wide")

# 💎 CLEAN CSS FOR YOUR LAYOUT
st.markdown("""
<style>
/* Hide Streamlit extras */
header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden !important; }

/* Page background */
body { background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%); }

/* Center everything */
.block-container { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }

/* Title styling */
h1 { 
    color: #e5e7eb !important; 
    font-size: 3rem !important; 
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 0.5rem !important;
}

/* Subtitle */
h3 { 
    color: #9ca3af !important; 
    font-size: 1.3rem !important; 
    font-weight: 400 !important;
    text-align: center;
    margin-bottom: 2.5rem !important;
}

/* 4 Toolkit Cards */
.toolkit-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.toolkit-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 1.8rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.toolkit-card:hover {
    transform: translateY(-8px);
    border-color: #6366f1;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
}

.toolkit-icon { 
    font-size: 2.2rem; 
    display: block; 
    margin-bottom: 0.8rem; 
}

.toolkit-title { 
    font-size: 1.1rem; 
    font-weight: 600; 
    color: #e5e7eb; 
    margin-bottom: 0.4rem;
}

.toolkit-desc { 
    font-size: 0.85rem; 
    color: #9ca3af; 
}

/* Chat Box */
.chat-box {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.chat-title {
    text-align: center;
    font-size: 1.4rem;
    color: #9ca3af;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* Chat messages */
.chat-box .stChatMessage {
    background: transparent !important;
    border: none !important;
    margin: 0.5rem 0 !important;
}

.chat-box [data-testid="stChatMessageContent"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 18px !important;
    padding: 1.2rem !important;
}

/* Chat input */
/* NEW - shorter */
/* Chat Box - Slimmer Version */
.chat-box {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px;
    padding: 2.5rem;
    margin: 0 auto 1.5rem auto; /* Added margin auto for centering */
    max-width: 700px;           /* Reduced from the default 900px */
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.chat-box textarea {
    background: transparent !important;
    border: none !important;
    color: #e5e7eb !important;
    font-size: 1rem !important;
}

.chat-box button[kind="secondary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
}

/* Caption */
.caption {
    text-align: center;
    color: #9ca3af;
    font-size: 1.1rem;
    font-style: italic;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# 💾 Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I can help you fix things step by step."}
    ]

# 🎯 MAIN TITLE (matches your sketch)
st.title("🛠️ AI DIY Home Improvement Guide")
st.markdown("### 🧰 DIY Toolkit")

# 🧰 4 TOOLKIT CARDS (exactly like sketch)
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

# 💬 CHAT BOX (matches your sketch)
st.markdown("""
<div class="chat-box">
    <div class="chat-title">Write your DIY question</div>
""", unsafe_allow_html=True)

# Show messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input inside chat box
user_input = st.chat_input("Ask your DIY question...")

st.markdown("</div>", unsafe_allow_html=True)

# ⚙️ Process input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("🔍 Thinking..."):
        reply = get_gemini_response(user_input)

    if reply is None or "error" in str(reply).lower():
        reply = fallback_response(user_input)
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()