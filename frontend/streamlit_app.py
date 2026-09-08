import os
import uuid
import requests
import streamlit as st

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000") + "/chat"

st.set_page_config(
    page_title="Darukaa.Earth Biodiversity Assistant",
    page_icon="🌿",
    layout="centered",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Dark forest palette */
        .stApp {
            background:
                radial-gradient(1200px 600px at 80% -10%, rgba(46, 204, 113, 0.12), transparent 60%),
                radial-gradient(900px 500px at -10% 110%, rgba(52, 152, 219, 0.10), transparent 60%),
                #0e1a12;
            color: #e8f2ea;
        }

        h1, h2, h3, .stApp h1 {
            font-family: 'Sora', sans-serif;
            color: #eaf6ee;
        }

        /* Hero header */
        .dk-hero {
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.16), rgba(39, 174, 96, 0.08));
            border: 1px solid rgba(46, 204, 113, 0.25);
            border-radius: 18px;
            padding: 22px 26px;
            margin-bottom: 18px;
        }
        .dk-hero h1 {
            margin: 0 0 6px 0;
            font-size: 1.65rem;
            letter-spacing: -0.02em;
        }
        .dk-hero p {
            margin: 0;
            color: #a8c3b0;
            font-size: 0.95rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #0b140e;
            border-right: 1px solid rgba(46, 204, 113, 0.15);
        }
        section[data-testid="stSidebar"] * {
            color: #cfe4d6 !important;
        }

        /* Chat bubbles */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 16px;
            padding: 12px 16px;
        }

        /* Recommendation cards */
        .dk-card {
            background: linear-gradient(160deg, rgba(46, 204, 113, 0.10), rgba(255, 255, 255, 0.03));
            border: 1px solid rgba(46, 204, 113, 0.22);
            border-radius: 14px;
            padding: 16px 18px;
            margin: 10px 0;
        }
        .dk-card h4 {
            margin: 0 0 8px 0;
            color: #7ef0a8;
            font-family: 'Sora', sans-serif;
            font-size: 1rem;
        }
        .dk-card p { margin: 5px 0; color: #d7e8dc; font-size: 0.92rem; }

        .dk-badge {
            display: inline-block;
            background: rgba(46, 204, 113, 0.15);
            border: 1px solid rgba(46, 204, 113, 0.35);
            color: #8df0ae;
            border-radius: 999px;
            padding: 2px 12px;
            font-size: 0.76rem;
            font-weight: 600;
            margin: 6px 8px 0 0;
        }
        .dk-badge.dim {
            background: rgba(93, 173, 226, 0.12);
            border-color: rgba(93, 173, 226, 0.35);
            color: #9fc8ec;
        }
        .dk-src {
            margin-top: 10px;
            color: #7d9a87;
            font-size: 0.78rem;
        }

        /* Buttons */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #27ae60, #1e8449);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 16px;
            font-weight: 600;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(46, 204, 113, 0.35);
            color: white;
        }

        /* Chat input */
        [data-testid="stChatInput"] textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #eaf6ee !important;
            border-radius: 14px !important;
        }

        /* Footer */
        .dk-footer {
            text-align: center;
            color: #6f8f7a;
            font-size: 0.8rem;
            margin-top: 26px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🌿 Darukaa.Earth")
    st.markdown("*Biodiversity Intelligence*")
    st.divider()
    st.markdown("**Ask me about**")
    st.markdown("🪨 Soil health & organic carbon  \n💧 Moisture & climate  \n🐦 Species & habitat  \n🌳 Land restoration")
    st.divider()
    if st.button("🔄 New conversation"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    st.caption("Powered by the Priyank Bansal as a Biodiversity Intelligence Chatbot.")

# ---------------------------------------------------------------- header
st.markdown(
    """
    <div class="dk-hero">
        <h1>🌿 Biodiversity Intelligence Chatbot</h1>
        <p>Ask about your land's biodiversity, soil, or climate conditions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_recommendations(recommendations: list[dict]) -> None:
    for i, rec in enumerate(recommendations, start=1):
        badges = "".join(
            f'<span class="dk-badge dim">⏱ {rec["time_horizon"].replace("_", " ")}</span>'
            f'<span class="dk-badge dim">🎯 Confidence: {rec.get("confidence", "n/a")}</span>'
        )
        effect = (
            f'<p><strong>📈 Estimated effect:</strong> {rec["estimated_effect"]}</p>'
            if rec.get("estimated_effect")
            else ""
        )
        st.markdown(
            f"""
            <div class="dk-card">
                <h4>{i}. {rec['action']}</h4>
                <p><em>Why it works:</em> {rec['mechanism']}</p>
                <p><strong>Impacted metrics:</strong> {', '.join(rec['impacted_metrics'])}</p>
                {effect}
                {badges}
                <div class="dk-src">Source: {rec['source']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=("🧑‍🌾" if msg["role"] == "user" else "🌿")):
        if msg.get("recommendations"):
            render_recommendations(msg["recommendations"])
        else:
            st.write(msg["content"])

st.markdown('<div class="dk-footer">🌱 Grown with care by Darukaa.Earth</div>', unsafe_allow_html=True)

user_message = st.chat_input("Describe your land, soil, or ask a question...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.write(user_message)

    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("🌿 Analyzing your land..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"session_id": st.session_state.session_id, "message": user_message},
                    timeout=90,
                )
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.Timeout:
                st.error(
                    "The backend took too long to respond — make sure it is running "
                    "(uvicorn app.main:app) and try again."
                )
                st.stop()
            except requests.RequestException as e:
                st.error(f"Couldn't reach the backend: {e}")
                st.stop()

        recommendations = data.get("recommendations", [])
        if recommendations:
            st.write(data["message"])
            render_recommendations(recommendations)
            st.session_state.messages.append({
                "role": "assistant",
                "content": data["message"],
                "recommendations": recommendations,
            })
        else:
            st.write(data["message"])
            st.session_state.messages.append({"role": "assistant", "content": data["message"]})