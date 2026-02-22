"""
ludy1_app.py - Ludy 1 Streamlit Web App
Built by BotDevelopmentAI
-----------------------------------------
Deploy to Streamlit Cloud (free): https://streamlit.io/cloud

When your ngrok URL changes, just update the one line below:
  SERVER_URL = "https://YOUR-URL-HERE.ngrok-free.app"
Then commit to GitHub — Streamlit auto-reloads in ~30 seconds.
"""

import streamlit as st
import requests
import time
import base64
from io import BytesIO
from PIL import Image

# ══════════════════════════════════════════════════════════════════
#  ↓↓↓  ONLY LINE YOU EVER NEED TO CHANGE  ↓↓↓
SERVER_URL = "https://ruthenious-unconsiderablely-aryanna.ngrok-free.dev"
#  ↑↑↑  PASTE YOUR NGROK URL ABOVE  ↑↑↑
# ══════════════════════════════════════════════════════════════════

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ludy 1 — BotDevelopmentAI",
    page_icon="🎨",
    layout="centered",
)

# ── Styling ────────────────────────────────────────────────────────
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
#MainMenu, footer, header { visibility: hidden; }

.ludy-header { text-align: center; padding: 32px 0 8px; }
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
.ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 0;
}
.ring-container { position: relative; width: 120px; height: 120px; }
.ring-svg { transform: rotate(-90deg); }
.ring-bg  { fill: none; stroke: #222; stroke-width: 6; }
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
.ring-pct    { font-size: 22px; color: #ff6b2b; line-height: 1; }
.ring-status { font-size: 9px; color: #555; letter-spacing: 1px; text-transform: uppercase; margin-top: 4px; }
.ring-caption { margin-top: 16px; font-size: 12px; color: #555; text-align: center; letter-spacing: 1px; }

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
.cancel-btn > button {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #888 !important;
}
.dl-btn {
    display: block;
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
.offline-msg {
    text-align: center;
    padding: 32px;
    background: #111;
    border: 1px solid #222;
    border-radius: 16px;
    color: #555;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────
def progress_ring(pct: int, status_text: str, caption: str = "") -> str:
    r      = 52
    circ   = 2 * 3.14159 * r
    offset = circ * (1 - pct / 100)
    return f"""
    <div class="ring-wrap">
      <div class="ring-container">
        <svg class="ring-svg" width="120" height="120" viewBox="0 0 120 120">
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
    img_data = b64_str.split(",")[1] if "," in b64_str else b64_str
    filename = f"ludy1_{int(time.time())}.png"
    return f'<a class="dl-btn" href="data:image/png;base64,{img_data}" download="{filename}">⬇ Download Image</a>'

def server_online() -> bool:
    try:
        r = requests.get(f"{SERVER_URL}/health", timeout=4)
        return r.status_code == 200
    except:
        return False


# ── Session state ──────────────────────────────────────────────────
for key, default in {
    "job_id":     None,
    "last_image": None,
    "history":    [],
    "cancelled":  False,
    "generating": False,
    "last_prompt": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Header ─────────────────────────────────────────────────────────
st.markdown("""
<div class="ludy-header">
  <div class="ludy-title">Ludy 1</div>
  <div class="ludy-sub">Image Generator · BotDevelopmentAI</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Server offline check ───────────────────────────────────────────
if not server_online():
    st.markdown("""
    <div class="offline-msg">
      ⚠️ Generator is currently offline.<br>
      <span style="font-size:11px;color:#444">The BotDevelopmentAI team will have it back up soon.</span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Controls (disabled while generating) ──────────────────────────
st.markdown("### ✏️ Describe your image")

prompt = st.text_area(
    "Prompt",
    placeholder="A cinematic photo of a golden retriever on a misty mountain at sunrise, professional photography, 8k...",
    height=100,
    label_visibility="collapsed",
    disabled=st.session_state.generating,
)

neg_prompt = st.text_area(
    "Negative prompt (what to avoid)",
    value="blurry, low quality, distorted, ugly, bad anatomy, watermark, text",
    height=68,
    disabled=st.session_state.generating,
)

col1, col2 = st.columns(2)
with col1:
    size = st.selectbox(
        "Size",
        ["512×512", "768×768", "1024×1024", "512×768", "768×512"],
        index=0,
        disabled=st.session_state.generating,
    )
    w, h = [int(x) for x in size.split("×")]
with col2:
    steps    = st.slider("Steps",          10, 50,   10,  disabled=st.session_state.generating)
    guidance = st.slider("Guidance Scale",  1.0, 15.0, 7.5, 0.5, disabled=st.session_state.generating)

# Generate OR Cancel button
if not st.session_state.generating:
    generate_clicked = st.button("🎨 GENERATE")
    cancel_clicked   = False
else:
    generate_clicked = False
    st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
    cancel_clicked = st.button("✕ CANCEL")
    st.markdown('</div>', unsafe_allow_html=True)


# ── Submit job ─────────────────────────────────────────────────────
if generate_clicked:
    if not prompt.strip():
        st.error("Please enter a prompt!")
    else:
        try:
            res = requests.post(
                f"{SERVER_URL}/generate",
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
            st.session_state.job_id      = data["job_id"]
            st.session_state.last_prompt = prompt
            st.session_state.cancelled   = False
            st.session_state.generating  = True
            st.session_state.last_image  = None
            st.rerun()
        except Exception as e:
            st.error(f"Could not reach server: {e}")

# ── Cancel ─────────────────────────────────────────────────────────
if cancel_clicked:
    try:
        requests.post(f"{SERVER_URL}/cancel/{st.session_state.job_id}", timeout=3)
    except:
        pass
    st.session_state.cancelled   = True
    st.session_state.generating  = False
    st.session_state.job_id      = None
    st.info("Generation cancelled.")
    st.rerun()


# ── Poll for result ────────────────────────────────────────────────
if st.session_state.job_id and st.session_state.generating:
    output_slot = st.empty()

    try:
        res    = requests.get(f"{SERVER_URL}/status/{st.session_state.job_id}", timeout=5)
        status = res.json()
        s      = status.get("status", "queued")

        if s == "queued":
            pos = status.get("queue_pos", "?")
            output_slot.markdown(
                progress_ring(10, "QUEUED", f"Position {pos} in queue — waiting for GPU..."),
                unsafe_allow_html=True,
            )
            time.sleep(30)
            st.rerun()

        elif s == "generating":
            pct = status.get("progress", 0)
            pct = max(5, pct)  # always show at least 5% so ring is visible
            output_slot.markdown(
                progress_ring(pct, "GENERATING", f"Step {pct}% complete — GPU working..."),
                unsafe_allow_html=True,
            )
            time.sleep(30)
            st.rerun()

        elif s == "done":
            output_slot.markdown(progress_ring(100, "DONE", ""), unsafe_allow_html=True)
            time.sleep(0.4)
            output_slot.empty()
            st.session_state.last_image = status["image"]
            st.session_state.history.insert(0, {
                "image":  status["image"],
                "prompt": st.session_state.last_prompt,
            })
            if len(st.session_state.history) > 12:
                st.session_state.history = st.session_state.history[:12]
            st.session_state.job_id     = None
            st.session_state.generating = False
            st.rerun()

        elif s == "error":
            st.error(f"Generation failed: {status.get('error', 'unknown error')}")
            st.session_state.job_id     = None
            st.session_state.generating = False
            st.rerun()

    except Exception as e:
        st.warning(f"Waiting for server... ({e})")
        time.sleep(2)
        st.rerun()


# ── Show result image ──────────────────────────────────────────────
if st.session_state.last_image and not st.session_state.generating:
    st.markdown("### 🖼️ Result")
    img_data = st.session_state.last_image.split(",")[1]
    img      = Image.open(BytesIO(base64.b64decode(img_data)))
    st.image(img, use_container_width=True)
    st.markdown(get_download_link(st.session_state.last_image), unsafe_allow_html=True)

    if st.button("Generate another"):
        st.session_state.last_image = None
        st.rerun()


# ── History ────────────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.markdown("### 🗂️ History")
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.history[:8]):
        with cols[i % 4]:
            img_data = item["image"].split(",")[1]
            img      = Image.open(BytesIO(base64.b64decode(img_data)))
            st.image(img, caption=item["prompt"][:35] + "...", use_container_width=True)


# ── Footer ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#333;font-size:11px;letter-spacing:2px">LUDY 1 · BOTDEVELOPMENTAI · POWERED BY LUDY 1.0</p>',
    unsafe_allow_html=True,
)
