import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="City Agent",
    page_icon="🏙️",
    layout="wide"
)

# =========================
# Custom CSS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

* { font-family: 'Syne', sans-serif; }
code, pre { font-family: 'Space Mono', monospace; }

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Title */
.agent-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    padding: 1rem 0 0.2rem;
    letter-spacing: -1px;
}

.agent-subtitle {
    text-align: center;
    color: #555570;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Chat messages */
.chat-container {
    max-height: 520px;
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    background: #0d0d18;
    margin-bottom: 1rem;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.6rem 0;
}

.msg-bot {
    display: flex;
    justify-content: flex-start;
    margin: 0.6rem 0;
}

.bubble-user {
    background: linear-gradient(135deg, #7b2fff, #00d4ff);
    color: white;
    padding: 0.7rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.5;
}

.bubble-bot {
    background: #1a1a2e;
    color: #e8e8f0;
    padding: 0.7rem 1.1rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.6;
    border: 1px solid #2a2a3e;
}

.bubble-system {
    background: #0f1f0f;
    color: #44ff88;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    border: 1px solid #1a3a1a;
    margin: 0.3rem 0;
    max-width: 90%;
}

.bubble-denied {
    background: #1f0f0f;
    color: #ff6b6b;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    border: 1px solid #3a1a1a;
    margin: 0.3rem 0;
    max-width: 90%;
}

/* Tool approval box */
.approval-box {
    background: #111128;
    border: 1px solid #7b2fff;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}

.approval-title {
    color: #7b2fff;
    font-weight: 600;
    font-size: 0.88rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.approval-detail {
    color: #888899;
    font-size: 0.82rem;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.8rem;
}

/* Input */
.stTextInput input {
    background: #0d0d18 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    padding: 0.7rem 1rem !important;
}

.stTextInput input:focus {
    border-color: #7b2fff !important;
    box-shadow: 0 0 0 2px rgba(123, 47, 255, 0.2) !important;
}

/* Buttons */
.stButton button {
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s !important;
}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: #08080f !important;
    border-right: 1px solid #1e1e2e !important;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #44ff88;
    margin-right: 6px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.stat-card {
    background: #0d0d18;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
    margin: 0.3rem 0;
}

.stat-number {
    font-size: 1.6rem;
    font-weight: 800;
    color: #7b2fff;
}

.stat-label {
    font-size: 0.72rem;
    color: #555570;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# Tools
# =========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    feels_like = data["main"]["feels_like"]
    return f"🌡️ {city}: {desc}, {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%"


@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )
    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"
    news_list = []
    for r in results:
        title = r.get("title", "No title")
        snippet = r.get("content", "")
        news_list.append(f"• {title}\n  {snippet[:120]}...")
    return f"📰 Latest news in {city}:\n\n" + "\n\n".join(news_list)


TOOLS = {
    "get_weather": get_weather,
    "get_news": get_news
}

TOOL_ICONS = {
    "get_weather": "🌦️",
    "get_news": "📰"
}


# =========================
# Session State
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_tool_calls" not in st.session_state:
    st.session_state.pending_tool_calls = []

if "pending_result" not in st.session_state:
    st.session_state.pending_result = None

if "tool_count" not in st.session_state:
    st.session_state.tool_count = 0

if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0


# =========================
# LLM
# =========================

@st.cache_resource
def get_llm():
    llm = ChatMistralAI(model="mistral-small-latest")
    return llm.bind_tools([get_weather, get_news])

llm_with_tools = get_llm()


# =========================
# UI — Header
# =========================

st.markdown('<div class="agent-title">🏙️ City Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="agent-subtitle">Powered by Mistral AI • Human in the Loop</div>', unsafe_allow_html=True)


# =========================
# Sidebar
# =========================

with st.sidebar:
    st.markdown("### <span class='status-dot'></span> Agent Status", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.msg_count}</div>
            <div class="stat-label">Messages</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.tool_count}</div>
            <div class="stat-label">Tools Used</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛠️ Available Tools")
    st.markdown("🌦️ **get_weather** — City weather")
    st.markdown("📰 **get_news** — Latest city news")

    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.code("What's the weather in Mumbai?")
    st.code("Latest news from Delhi?")
    st.code("Weather and news for Indore?")

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.pending_tool_calls = []
        st.session_state.pending_result = None
        st.session_state.tool_count = 0
        st.session_state.msg_count = 0
        st.rerun()


# =========================
# Chat Display
# =========================

chat_html = '<div class="chat-container">'

if not st.session_state.chat_history:
    chat_html += '<div style="text-align:center; color:#333355; padding: 3rem 0; font-size:0.85rem;">Start by asking about any city! 🌍</div>'
else:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-user"><div class="bubble-user">👤 {msg["content"]}</div></div>'
        elif msg["role"] == "assistant":
            chat_html += f'<div class="msg-bot"><div class="bubble-bot">🤖 {msg["content"]}</div></div>'
        elif msg["role"] == "tool_used":
            chat_html += f'<div class="msg-bot"><div class="bubble-system">✅ Tool executed: {msg["content"]}</div></div>'
        elif msg["role"] == "tool_denied":
            chat_html += f'<div class="msg-bot"><div class="bubble-denied">❌ Tool denied: {msg["content"]}</div></div>'

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)


# =========================
# Human Approval UI
# =========================

if st.session_state.pending_tool_calls:
    tool_call = st.session_state.pending_tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    icon = TOOL_ICONS.get(tool_name, "🔧")

    st.markdown(f"""
    <div class="approval-box">
        <div class="approval-title">🔔 Tool Approval Required</div>
        <div class="approval-detail">Tool: {icon} {tool_name} | Args: {tool_args}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve", use_container_width=True, type="primary"):
            tool_message = TOOLS[tool_name].invoke(tool_call)
            st.session_state.messages.append(tool_message)
            st.session_state.chat_history.append({
                "role": "tool_used",
                "content": f"{icon} {tool_name}({tool_args})"
            })
            st.session_state.tool_count += 1
            st.session_state.pending_tool_calls.pop(0)

            if not st.session_state.pending_tool_calls:
                final_result = llm_with_tools.invoke(st.session_state.messages)
                st.session_state.messages.append(final_result)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": final_result.content
                })

            st.rerun()

    with col2:
        if st.button("❌ Deny", use_container_width=True):
            from langchain_core.messages import ToolMessage as TM
            denied_msg = TM(
                content="Tool call denied by user.",
                tool_call_id=tool_call["id"]
            )
            st.session_state.messages.append(denied_msg)
            st.session_state.chat_history.append({
                "role": "tool_denied",
                "content": f"{icon} {tool_name}"
            })
            st.session_state.pending_tool_calls.pop(0)

            if not st.session_state.pending_tool_calls:
                final_result = llm_with_tools.invoke(st.session_state.messages)
                st.session_state.messages.append(final_result)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": final_result.content
                })

            st.rerun()


# =========================
# Input
# =========================

if not st.session_state.pending_tool_calls:
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "",
                placeholder="Ask about any city... e.g. 'Weather in Mumbai'",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send →", use_container_width=True, type="primary")

        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.messages.append(HumanMessage(user_input))
            st.session_state.msg_count += 1

            result = llm_with_tools.invoke(st.session_state.messages)
            st.session_state.messages.append(result)

            if result.tool_calls:
                st.session_state.pending_tool_calls = result.tool_calls
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result.content
                })

            st.rerun()