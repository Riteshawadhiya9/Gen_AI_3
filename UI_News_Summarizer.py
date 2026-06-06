from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import time
from datetime import datetime
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PulseAI — Live News Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #050507;
    --surface:   #0d0d12;
    --border:    #1a1a24;
    --accent:    #e8ff47;
    --accent2:   #ff6b35;
    --muted:     #3a3a50;
    --text:      #d8d8e8;
    --text-dim:  #5a5a78;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
}

#MainMenu, footer, header { visibility: hidden; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--muted); border-radius: 2px; }

/* ── layout ── */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem !important;
}

/* ── main area padding ── */
.main-pad { padding: 2.5rem 3rem; }

/* ── hero header ── */
.hero {
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.8rem;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    letter-spacing: 0.04em;
    line-height: 0.9;
    color: #fff;
    margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 0.75rem;
    color: var(--text-dim);
    margin-top: 0.7rem;
    letter-spacing: 0.05em;
}

/* ── ticker ── */
.ticker-wrap {
    background: var(--accent);
    padding: 0.35rem 0;
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 2rem;
}
.ticker-inner {
    display: inline-block;
    animation: ticker 28s linear infinite;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.9rem;
    letter-spacing: 0.12em;
    color: #050507;
}
@keyframes ticker {
    0%   { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

/* ── search bar ── */
div[data-testid="stTextInput"] input {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,255,71,0.08) !important;
}

/* ── buttons ── */
div.stButton > button {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: var(--accent) !important;
    color: #050507 !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.6rem 1.6rem !important;
    transition: opacity 0.15s, transform 0.1s;
    width: 100%;
}
div.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px);
}
div.stButton > button:active { transform: translateY(0); }

/* secondary button */
.sec-btn div.stButton > button {
    background: transparent !important;
    color: var(--text-dim) !important;
    border: 1px solid var(--border) !important;
}
.sec-btn div.stButton > button:hover {
    border-color: var(--muted) !important;
    color: var(--text) !important;
}

/* ── result card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent);
}
.result-card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.1em;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.result-body {
    font-size: 0.83rem;
    line-height: 1.8;
    color: var(--text);
}
.result-body ul { padding-left: 1.2rem; margin: 0; }
.result-body li { margin-bottom: 0.5rem; }

/* ── meta chips ── */
.meta-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1.2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
.chip {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--text-dim);
}
.chip.green  { border-color: #2d5a2d; color: #5aab5a; background: #0d1f0d; }
.chip.orange { border-color: #5a3010; color: #ff8c50; background: #1f1008; }
.chip.yellow { border-color: #4a4a10; color: var(--accent); background: #1a1a05; }

/* ── source list ── */
.source-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.85rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.75rem;
}
.source-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    color: var(--accent);
    min-width: 24px;
    line-height: 1;
    margin-top: 1px;
}
.source-url { color: var(--text-dim); word-break: break-all; }
.source-title { color: var(--text); margin-bottom: 0.2rem; }

/* ── sidebar section labels ── */
.sidebar-label {
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 0.6rem;
    margin-top: 1.4rem;
    display: block;
}
.sidebar-label:first-child { margin-top: 0; }

/* ── history item ── */
.hist-item {
    padding: 0.6rem 0.8rem;
    border-radius: 5px;
    border: 1px solid var(--border);
    margin-bottom: 0.4rem;
    font-size: 0.73rem;
    color: var(--text-dim);
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
    word-break: break-word;
}
.hist-item:hover { border-color: var(--muted); color: var(--text); }

/* ── status ── */
.status-live {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5aab5a;
}
.pulse-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #5aab5a;
    animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.7); }
}

/* ── spinner override ── */
div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}

/* ── toast / info box ── */
div[data-testid="stInfo"] {
    background: #0d1a0d !important;
    border: 1px solid #1a3a1a !important;
    border-radius: 6px !important;
    color: #7acc7a !important;
}

/* ── select box ── */
div[data-testid="stSelectbox"] select,
div[data-baseweb="select"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── slider ── */
div[data-testid="stSlider"] .st-emotion-cache-1inwz65 {
    background: var(--accent) !important;
}

/* ── tabs ── */
button[data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []
if "last_ts" not in st.session_state:
    st.session_state.last_ts = ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                    letter-spacing:0.1em;color:#fff;line-height:1;">
            PULSE<span style="color:#e8ff47;">AI</span>
        </div>
        <div style="font-size:0.6rem;letter-spacing:0.2em;
                    text-transform:uppercase;color:#3a3a50;margin-top:2px;">
            News Intelligence Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sidebar-label">Search Config</span>', unsafe_allow_html=True)
    max_results = st.slider("Max sources", min_value=3, max_value=10, value=5, step=1)

    st.markdown('<span class="sidebar-label">Output Style</span>', unsafe_allow_html=True)
    output_style = st.selectbox(
        "Format",
        ["Bullet Points", "Executive Brief", "Deep Analysis"],
        label_visibility="collapsed",
    )

    st.markdown('<span class="sidebar-label">Search History</span>', unsafe_allow_html=True)
    if st.session_state.history:
        for h in reversed(st.session_state.history[-8:]):
            st.markdown(f'<div class="hist-item">⚡ {h}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.7rem;color:#3a3a50;">No searches yet.</div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.62rem;color:#3a3a50;line-height:1.7;">
        Powered by<br>
        <span style="color:#5a5a78;">Mistral · Tavily · LangChain</span>
    </div>
    """, unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-pad">', unsafe_allow_html=True)

# hero
now = datetime.now().strftime("%d %b %Y  ·  %H:%M")
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">⚡ Live Intelligence Feed</div>
    <h1 class="hero-title">PULSE<span>AI</span></h1>
    <div class="hero-sub">
        Real-time news · AI-synthesized summaries · {now}
    </div>
</div>
""", unsafe_allow_html=True)

# ticker
st.markdown("""
<div class="ticker-wrap">
    <span class="ticker-inner">
        ⚡ LIVE  &nbsp;·&nbsp;  AI News Intelligence  &nbsp;·&nbsp;
        Powered by Mistral &amp; Tavily  &nbsp;·&nbsp;
        Real-time Web Search  &nbsp;·&nbsp;
        AI-Synthesized Summaries  &nbsp;·&nbsp;
        ⚡ LIVE  &nbsp;·&nbsp;  AI News Intelligence  &nbsp;·&nbsp;
        Powered by Mistral &amp; Tavily  &nbsp;·&nbsp;
        Real-time Web Search  &nbsp;·&nbsp;
        AI-Synthesized Summaries  &nbsp;·&nbsp;
    </span>
</div>
""", unsafe_allow_html=True)

# ── Search bar ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    query = st.text_input(
        "query",
        placeholder="e.g. latest AI breakthroughs 2026  ·  geopolitical tensions in Asia  ·  climate tech news",
        label_visibility="collapsed",
        value=st.session_state.last_query,
    )
with col_btn:
    search_clicked = st.button("⚡ Search", use_container_width=True)

# ── Quick topics ──────────────────────────────────────────────────────────────
st.markdown('<div style="margin:0.7rem 0 1.5rem;">', unsafe_allow_html=True)
qt_cols = st.columns(6)
quick_topics = ["AI 2026", "Space Tech", "Crypto", "Climate", "Geopolitics", "Biotech"]
chosen_topic = None
for i, topic in enumerate(quick_topics):
    with qt_cols[i]:
        if st.button(topic, key=f"qt_{i}"):
            chosen_topic = f"latest news on {topic} 2026"
st.markdown('</div>', unsafe_allow_html=True)

# resolve query
active_query = chosen_topic if chosen_topic else (query if search_clicked else None)

# ── Prompt templates ──────────────────────────────────────────────────────────
STYLE_PROMPTS = {
    "Bullet Points": """
You are a senior news analyst. Summarize the following news into clear, concise bullet points.
Each bullet should be one crisp sentence. Group related points if possible. Max 8 bullets.
{news}
""",
    "Executive Brief": """
You are a C-suite briefing writer. Write a tight executive brief (3 short paragraphs: 
Overview, Key Developments, Implications) from the following news. Be direct and sharp.
{news}
""",
    "Deep Analysis": """
You are an investigative journalist. Write a deep analytical summary covering:
1. What happened
2. Why it matters
3. Who is affected
4. What to watch next
Use the following news as your source material.
{news}
""",
}

# ── Run search ────────────────────────────────────────────────────────────────
if active_query:
    with st.spinner("Scanning live sources..."):
        try:
            search_tool = TavilySearchResults(max_results=max_results)
            llm = ChatMistralAI(model="mistral-small-2506")
            prompt_template = ChatPromptTemplate.from_template(STYLE_PROMPTS[output_style])
            chain = prompt_template | llm | StrOutputParser()

            raw_results = search_tool.invoke(active_query)
            news_text = "\n\n".join(
                [f"Source: {r.get('url','')}\nTitle: {r.get('title','')}\nContent: {r.get('content','')}"
                 for r in raw_results]
            ) if isinstance(raw_results, list) else str(raw_results)

            result = chain.invoke({"news": news_text})

            st.session_state.last_result = result
            st.session_state.last_query = active_query
            st.session_state.last_sources = raw_results if isinstance(raw_results, list) else []
            st.session_state.last_ts = datetime.now().strftime("%H:%M:%S")

            if active_query not in st.session_state.history:
                st.session_state.history.append(active_query)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.last_result:
    tab1, tab2 = st.tabs(["📰  Summary", "🔗  Sources"])

    with tab1:
        src_count = len(st.session_state.last_sources)
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-title">
                <span>📰</span> AI SUMMARY
            </div>
            <div class="result-body">
                {st.session_state.last_result.replace(chr(10), '<br>')}
            </div>
            <div class="meta-row">
                <span class="chip green">✓ Live data</span>
                <span class="chip yellow">⚡ {output_style}</span>
                <span class="chip orange">⏱ {st.session_state.last_ts}</span>
                <span class="chip">{src_count} sources</span>
                <span class="chip">Mistral Small 2506</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # copy area
        st.text_area(
            "Raw output (copy)",
            value=st.session_state.last_result,
            height=180,
            label_visibility="collapsed",
        )

    with tab2:
        if st.session_state.last_sources:
            st.markdown(f"""
            <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
                        color:#5a5a78;margin-bottom:1rem;">
                {len(st.session_state.last_sources)} Sources Retrieved
            </div>
            """, unsafe_allow_html=True)

            for i, src in enumerate(st.session_state.last_sources, 1):
                title = src.get("title", "Untitled") if isinstance(src, dict) else "Source"
                url   = src.get("url", "") if isinstance(src, dict) else ""
                content = src.get("content", "")[:200] + "..." if isinstance(src, dict) else ""
                st.markdown(f"""
                <div class="source-item">
                    <span class="source-num">{i:02d}</span>
                    <div>
                        <div class="source-title">{title}</div>
                        <div class="source-url">{url}</div>
                        <div style="color:#3a3a50;font-size:0.7rem;margin-top:0.3rem;">{content}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#3a3a50;font-size:0.8rem;">No source data available.</div>',
                        unsafe_allow_html=True)

elif not active_query:
    # empty state
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;
                    color:#1a1a24;letter-spacing:0.1em;line-height:1;">
            READY TO<br>SCAN
        </div>
        <div style="font-size:0.72rem;color:#3a3a50;letter-spacing:0.12em;
                    text-transform:uppercase;margin-top:1rem;">
            Enter a topic above or pick a quick category
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-pad