"""
ludy1_app.py - Ludy 1 Streamlit Web App
Built by BotDevelopmentAI
-----------------------------------------
Deploy this to Streamlit Cloud for free.
Your laptop runs ludy1_server.py as the GPU backend.

Deploy at: https://streamlit.io/cloud
"""

import streamlit as st
import requests
import time
import base64
from io import BytesIO
from PIL import Image

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ludy 1 — BotDevelopmentAI",
    page_icon="🎨",
    layout="centered",
)

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #080808;
    color: #f0f0f0;
}

.stApp { background-color: #080808; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* Hide default streamlit stuff */
#MainMenu, footer, header { visibility: hidden; }

.ludy-header {
    text-align: center;
    padding: 32px 0 8px;
}

.ludy-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b2b, #ff3e6c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -2px;
    line-height: 1;
}

.ludy-sub {
    font-size: 12px;
    color: #555;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}

/* Ring progress */
.ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 0;
}

.ring-container {
    position: relative;
    width: 120px;
    height: 120px;
}

.ring-svg {
    transform: rotate(-90deg);
}

.ring-bg {
    fill: none;
    stroke: #222;
    stroke-width: 6;
}

.ring-fill {
    fill: none;
    stroke: url(#ringGrad);
    stroke-width: 6;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.5s ease;
}

.ring-label {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
}

.ring-pct {
    font-size: 22px;
    color: #ff6b2b;
    line-height: 1;
}

.ring-status {
    font-size: 9px;
    color: #555;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

.ring-caption {
    margin-top: 16px;
    font-size: 12px;
    color: #555;
    text-align: center;
    letter-spacing: 1px;
}

/* Download button */
.dl-btn {
    display: inline-block;
    padding: 12px 32px;
    background: linear-gradient(135deg, #ff6b2b, #ff3e6c);
    color: white !important;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1px;
    border-radius: 12px;
    text-decoration: none;
    text-align: center;
    margin-top: 12px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ff6b2b, #ff3e6c) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

.stTextArea textarea, .stTextInput input, .stSlider {
    background: #111 !important;
    border-color: #222 !important;
    color: #f0f0f0 !important;
    font-family: 'DM Mono', monospace !important;
}

.server-input {
    background: #111;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 12px 16px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #f0f0f0;
    width: 100%;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}
.dot-green { background: #00e5a0; }
.dot-red   { background: #ff3e6c; }
.dot-gray  { background: #444; }
</style>
""", unsafe_allow_html=True)


# ── Helper: progress ring HTML ─────────────────────────────────────────────────
def progress_ring(pct: int, status_text: str, caption: str = "") -> str:
    r          = 52
    circ       = 2 * 3.14159 * r
    offset     = circ * (1 - pct / 100)
    spin_class = "spinning" if pct < 100 else ""

    return f"""
    <div class="ring-wrap">
      <div class="ring-container">
        <svg class="ring-svg {spin_class}" width="120" height="120" viewBox="0 0 120 120">
          <defs>
            <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%"   stop-color="#ff6b2b"/>
              <stop offset="100%" stop-color="#ff3e6c"/>
            </linearGradient>
          </defs>
          <circle class="ring-bg"   cx="60" cy="60" r="{r}"/>
          <circle class="ring-fill" cx="60" cy="60" r="{r}"
            stroke-dasharray="{circ:.1f}"
            stroke-dashoffset="{offset:.1f}"/>
        </svg>
        <div class="ring-label">
          <span class="ring-pct">{pct}%</span>
          <span class="ring-status">{status_text}</span>
        </div>
      </div>
      <div class="ring-caption">{caption}</div>
    </div>
    """


def get_download_link(b64_str: str) -> str:
    # Strip the data URI prefix
    img_data = b64_str.split(",")[1] if "," in b64_str else b64_str
    filename = f"ludy1_{int(time.time())}.png"
    return f'<a class="dl-btn" href="data:image/png;base64,{img_data}" download="{filename}">⬇ Download Image</a>'


# ── Session state ──────────────────────────────────────────────────────────────
if "server_url" not in st.session_state:
    st.session_state.server_url = ""
if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "last_image" not in st.session_state:
    st.session_state.last_image = None
if "history" not in st.session_state:
    st.session_state.history = []


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ludy-header">
  <div class="ludy-title">Ludy 1</div>
  <div class="ludy-sub">Image Generator · BotDevelopmentAI</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ── Server connection ──────────────────────────────────────────────────────────
with st.expander("⚙️ Server Settings", expanded=st.session_state.server_url == ""):
    st.caption("Paste the public URL from your laptop (shown when you run start.bat)")
    server_url = st.text_input(
        "Your Laptop Server URL",
        value=st.session_state.server_url,
        placeholder="https://abc123.ngrok-free.app",
        label_visibility="collapsed",
    )
    if server_url:
        st.session_state.server_url = server_url.rstrip("/")

    if st.session_state.server_url:
        try:
            r = requests.get(f"{st.session_state.server_url}/health", timeout=5)
            if r.status_code == 200:
                st.markdown('<span class="status-dot dot-green"></span>Server online ✓', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-dot dot-red"></span>Server error', unsafe_allow_html=True)
        except:
            st.markdown('<span class="status-dot dot-red"></span>Cannot reach server — is start.bat running?', unsafe_allow_html=True)


# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("### ✏️ Describe your image")

prompt = st.text_area(
    "Prompt",
    placeholder="A cinematic photo of a golden retriever on a misty mountain at sunrise, professional photography, 8k...",
    height=100,
    label_visibility="collapsed",
)

neg_prompt = st.text_area(
    "Negative prompt (what to avoid)",
    value="blurry, low quality, distorted, ugly, bad anatomy, watermark, text",
    height=68,
)

col1, col2 = st.columns(2)
with col1:
    size = st.selectbox("Size", ["512×512", "768×768", "1024×1024", "512×768", "768×512"], index=1)
    w, h = [int(x) for x in size.split("×")]
with col2:
    steps    = st.slider("Steps", 10, 50, 30)
    guidance = st.slider("Guidance Scale", 1.0, 15.0, 7.5, 0.5)

generate_clicked = st.button("🎨 GENERATE")


# ── Generation logic ───────────────────────────────────────────────────────────
if generate_clicked:
    if not st.session_state.server_url:
        st.error("Please set your server URL above first!")
    elif not prompt.strip():
        st.error("Please enter a prompt!")
    else:
        try:
            res = requests.post(
                f"{st.session_state.server_url}/generate",
                json={
                    "prompt":          prompt,
                    "negative_prompt": neg_prompt,
                    "steps":           steps,
                    "width":           w,
                    "height":          h,
                    "guidance":        guidance,
                },
                timeout=10,
            )
            data = res.json()
            st.session_state.job_id = data["job_id"]
        except Exception as e:
            st.error(f"Could not reach server: {e}")


# ── Polling / display ──────────────────────────────────────────────────────────
if st.session_state.job_id and not st.session_state.last_image:
    output_slot = st.empty()
    done        = False

    while not done:
        try:
            res    = requests.get(f"{st.session_state.server_url}/status/{st.session_state.job_id}", timeout=5)
            status = res.json()

            s = status.get("status", "queued")

            if s == "queued":
                pos     = status.get("queue_pos", "?")
                caption = f"Position {pos} in queue — waiting for GPU..."
                output_slot.markdown(progress_ring(10, "QUEUED", caption), unsafe_allow_html=True)

            elif s == "generating":
                output_slot.markdown(progress_ring(60, "GENERATING", "GPU is working on your image..."), unsafe_allow_html=True)

            elif s == "done":
                output_slot.markdown(progress_ring(100, "DONE", ""), unsafe_allow_html=True)
                time.sleep(0.5)
                output_slot.empty()

                img_b64 = status["image"]
                st.session_state.last_image = img_b64
                st.session_state.history.insert(0, {"image": img_b64, "prompt": prompt})
                if len(st.session_state.history) > 12:
                    st.session_state.history = st.session_state.history[:12]
                st.session_state.job_id = None
                done = True
                st.rerun()

            elif s == "error":
                st.error(f"Generation failed: {status.get('error', 'unknown error')}")
                st.session_state.job_id = None
                done = True

        except Exception as e:
            output_slot.warning(f"Waiting for server... ({e})")

        if not done:
            time.sleep(2)


# ── Show last image ────────────────────────────────────────────────────────────
if st.session_state.last_image:
    st.markdown("### 🖼️ Result")

    # Display image
    img_data = st.session_state.last_image.split(",")[1]
    img      = Image.open(BytesIO(base64.b64decode(img_data)))
    st.image(img, use_container_width=True)

    # Download button
    st.markdown(get_download_link(st.session_state.last_image), unsafe_allow_html=True)

    if st.button("Generate another"):
        st.session_state.last_image = None
        st.rerun()


# ── History ────────────────────────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.markdown("### 🗂️ History")
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.history[:8]):
        with cols[i % 4]:
            img_data = item["image"].split(",")[1]
            img      = Image.open(BytesIO(base64.b64decode(img_data)))
            st.image(img, caption=item["prompt"][:40] + "...", use_container_width=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#333;font-size:11px;letter-spacing:2px">LUDY 1 · BOTDEVELOPMENTAI · POWERED BY SDXL</p>',
    unsafe_allow_html=True
)
