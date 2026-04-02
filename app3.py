import streamlit as st
import pickle

# ================= CONFIG =================
st.set_page_config(
    page_title="RecoAI — Smart Recommender",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= STYLE =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT ── */
:root {
    --bg:        #080c14;
    --surface:   #0f1623;
    --surface2:  #151e2e;
    --border:    rgba(99,179,237,0.10);
    --accent:    #38bdf8;
    --accent2:   #818cf8;
    --green:     #34d399;
    --amber:     #fbbf24;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --glow:      rgba(56,189,248,0.18);
}

/* ── GLOBAL ── */
html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem !important; }

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    padding: 0.55rem 0.9rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--glow) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 0.5rem 1.1rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── SESSION ITEMS ── */
.session-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 5px 12px;
    margin: 4px 3px;
    font-size: 13px;
    color: var(--accent);
    font-family: 'Syne', sans-serif;
    font-weight: 600;
}

/* ── REC CARD ── */
.rec-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.rec-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(56,189,248,0.15);
}
.rec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    border-radius: 18px 0 0 18px;
}

.rec-rank {
    position: absolute;
    top: 16px; right: 18px;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--muted);
    text-transform: uppercase;
}

.rec-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}

.rec-score {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 12px;
}
.rec-score span {
    color: var(--accent);
    font-weight: 600;
}

/* ── BADGES ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    margin: 3px 3px 3px 0;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.04em;
}
.badge-session    { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.badge-next       { background: rgba(56,189,248,0.12); color: #38bdf8; border: 1px solid rgba(56,189,248,0.25); }
.badge-co         { background: rgba(129,140,248,0.12); color: #818cf8; border: 1px solid rgba(129,140,248,0.25); }
.badge-popular    { background: rgba(251,191,36,0.12); color: #fbbf24;  border: 1px solid rgba(251,191,36,0.25); }

/* ── SIGNAL BARS ── */
.signal-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
    font-size: 12px;
    color: var(--muted);
}
.signal-label { width: 90px; text-align: right; font-family: 'DM Sans', sans-serif; }
.signal-track {
    flex: 1;
    height: 5px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
}
.signal-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.signal-val { width: 24px; font-weight: 600; color: var(--text); font-family: 'Syne', sans-serif; font-size: 11px; }

/* ── DIVIDER ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 20px 0;
}

/* ── LOGO ── */
.logo-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 28px;
}
.logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
}
.logo-text span { color: var(--accent); }

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--muted);
}
.empty-state .icon { font-size: 48px; margin-bottom: 14px; }
.empty-state p { font-size: 15px; }

/* ── STATS ROW ── */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    color: var(--muted);
    margin-right: 8px;
    margin-bottom: 18px;
}
.stat-pill b { color: var(--text); font-family: 'Syne', sans-serif; font-size: 13px; }

/* ── SECTION HEADER ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 18px 0 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
@st.cache_resource
def load_data():
    try:
        cooccur = pickle.load(open("cooccur.pkl", "rb"))
        cooccur = dict(list(cooccur.items())[:30000])
    except:
        cooccur = {}
    try:
        next_top = pickle.load(open("next_top.pkl", "rb"))
    except:
        next_top = {}
    try:
        popular_items = pickle.load(open("popular.pkl", "rb"))
    except:
        popular_items = list(range(1000))
    return cooccur, next_top, popular_items

cooccur, next_top, popular_items = load_data()

# ================= SESSION =================
if "session_items" not in st.session_state:
    st.session_state.session_items = []

# ================= MODEL =================
def recommend(session_items, k=6):
    if not session_items:
        return []
    results = []
    last_item = session_items[-1]
    session_set = set(session_items)
    candidates = set(popular_items[:150]) | session_set

    for aid in candidates:
        score = 0
        exp = {}
        if aid in session_set:
            score += 5; exp["Session"] = 5
        if last_item in next_top and aid in next_top[last_item]:
            score += 3; exp["Next-item"] = 3
        co_score = sum(
            2 for item in session_items
            if item in cooccur and aid in cooccur.get(item, {})
        ) if cooccur else 0
        if co_score > 0:
            score += co_score; exp["Co-occur"] = co_score
        if aid in popular_items[:100]:
            score += 1; exp["Popular"] = 1
        if score > 0:
            results.append((aid, score, exp))

    return sorted(results, key=lambda x: x[1], reverse=True)[:k]

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-icon">✦</div>
        <div class="logo-text">Reco<span>AI</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Add to Session</div>', unsafe_allow_html=True)
    new_item = st.text_input("Item ID", placeholder="e.g. 42", label_visibility="collapsed")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("➕  Add Item", use_container_width=True):
            if new_item.strip().isdigit():
                st.session_state.session_items.append(int(new_item.strip()))
                st.rerun()
            elif new_item.strip():
                st.warning("Enter a numeric ID")
    with col_b:
        if st.button("🗑  Clear All", use_container_width=True):
            st.session_state.session_items = []
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Session Queue</div>', unsafe_allow_html=True)

    if not st.session_state.session_items:
        st.markdown('<p style="color:var(--muted);font-size:13px;padding:8px 0;">No items yet.</p>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(st.session_state.session_items):
            c1, c2 = st.columns([3, 1])
            c1.markdown(f'<div class="session-tag">#{item}</div>', unsafe_allow_html=True)
            if c2.button("✕", key=f"rm_{i}"):
                st.session_state.session_items.pop(i)
                st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:11px;color:var(--muted);line-height:1.6;">
    Signals: <b style="color:var(--green)">Session</b> · 
    <b style="color:var(--accent)">Next-item</b> · 
    <b style="color:var(--accent2)">Co-occurrence</b> · 
    <b style="color:var(--amber)">Popularity</b>
    </p>
    """, unsafe_allow_html=True)

# ================= MAIN =================
st.markdown("""
<h1 style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;
           letter-spacing:-0.03em;margin-bottom:4px;">
  Session-Based Recommendations
</h1>
<p style="color:var(--muted);font-size:14px;margin-bottom:20px;">
  Real-time · Explainable signals · Production-ready
</p>
""", unsafe_allow_html=True)

n_items = len(st.session_state.session_items)
recs = recommend(st.session_state.session_items) if n_items else []

st.markdown(f"""
<span class="stat-pill">🧾 <b>{n_items}</b>&nbsp;items in session</span>
<span class="stat-pill">🔮 <b>{len(recs)}</b>&nbsp;recommendations</span>
<span class="stat-pill">📦 <b>{len(popular_items)}</b>&nbsp;catalog items</span>
""", unsafe_allow_html=True)

# ── Empty state ──
if not st.session_state.session_items:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🛍️</div>
        <p>Add item IDs in the sidebar to generate personalised recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Recommendations grid ──
BADGE_CLASS = {
    "Session":  "badge-session",
    "Next-item": "badge-next",
    "Co-occur": "badge-co",
    "Popular":  "badge-popular",
}

cols = st.columns(3)
for idx, (aid, score, exp) in enumerate(recs):
    with cols[idx % 3]:
        badges = "".join(
            f'<span class="badge {BADGE_CLASS.get(k,"badge-co")}">{k}</span>'
            for k in exp
        )
        max_score = max((v for v in exp.values()), default=1)
        bars = "".join(
            f"""
            <div class="signal-row">
                <div class="signal-label">{k}</div>
                <div class="signal-track">
                    <div class="signal-fill" style="width:{min(v/max(max_score,1)*100,100):.0f}%"></div>
                </div>
                <div class="signal-val">+{v}</div>
            </div>"""
            for k, v in exp.items()
        )
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-rank">#{idx+1}</div>
            <div class="rec-title">Item {aid}</div>
            <div class="rec-score">Score &nbsp;<span>{round(score, 2)}</span></div>
            <div style="margin-bottom:10px">{badges}</div>
            {bars}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Add #{aid} to session", key=f"add_{aid}_{idx}"):
            st.session_state.session_items.append(aid)
            st.rerun()