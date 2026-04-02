import streamlit as st
import pickle

# ================= CONFIG =================
st.set_page_config(page_title="RecoAI", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #0f172a);
    color: #e2e8f0;
}

/* CARD */
.card {
    background: rgba(15, 23, 42, 0.85);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 15px 50px rgba(0,0,0,0.7);
}

/* TOP RECOMMENDATION */
.top-card {
    border: 1px solid gold;
    box-shadow: 0 0 20px rgba(255,215,0,0.4);
}

/* BADGES */
.badge {
    padding:4px 10px;
    margin:4px;
    border-radius:20px;
    font-size:11px;
    font-weight:600;
}
.session {background:#064e3b;color:#34d399;}
.next {background:#0c4a6e;color:#38bdf8;}
.co {background:#312e81;color:#818cf8;}
.pop {background:#78350f;color:#fbbf24;}

/* BARS */
.bar-wrap {margin-top:6px;}
.bar-label {font-size:12px;color:#94a3b8;}
.bar-track {
    width:100%;
    height:6px;
    background:#1e293b;
    border-radius:10px;
}
.bar-fill {
    height:100%;
    border-radius:10px;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
}

/* SESSION ITEM */
.session-item {
    display:flex;
    justify-content:space-between;
    background:#1e293b;
    padding:6px 10px;
    border-radius:10px;
    margin-bottom:6px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD =================
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
            score += co_score; exp["Co"] = co_score

        if aid in popular_items[:100]:
            score += 1; exp["Popular"] = 1

        if score > 0:
            results.append((aid, score, exp))

    return sorted(results, key=lambda x: x[1], reverse=True)[:k]

# ================= HEADER =================
st.title("🛍️ RecoAI — Smart Recommender")
st.caption("Explainable • Fast • Premium UI")

col1, col2 = st.columns([1, 3])

# ================= LEFT =================
with col1:
    st.subheader("Session")

    new_item = st.text_input("Item ID")

    if st.button("Add"):
        if new_item.isdigit():
            st.session_state.session_items.append(int(new_item))

    if st.button("Clear"):
        st.session_state.session_items = []

    st.write("### Items")

    for i, item in enumerate(st.session_state.session_items):
        c1, c2 = st.columns([3,1])
        c1.markdown(f'<div class="session-item">Item {item}</div>', unsafe_allow_html=True)
        if c2.button("❌", key=f"remove_{i}"):
            st.session_state.session_items.pop(i)
            st.rerun()

# ================= RIGHT =================
with col2:
    st.subheader("Recommendations")

    if not st.session_state.session_items:
        st.info("Add items to start")
    else:
        recs = recommend(st.session_state.session_items)
        cols = st.columns(2)

        for idx, (aid, score, exp) in enumerate(recs):
            with cols[idx % 2]:

                # TOP highlight
                card_class = "card top-card" if idx == 0 else "card"

                # badges
                badge_html = ""
                for k in exp:
                    cls = {
                        "Session": "session",
                        "Next-item": "next",
                        "Co": "co",
                        "Popular": "pop"
                    }.get(k, "co")
                    badge_html += f'<span class="badge {cls}">{k}</span>'

                # bars
                max_score = max(exp.values()) if exp else 1
                bars_html = ""

                for k, v in exp.items():
                    width = int((v / max_score) * 100)
                    bars_html += (
                        f'<div class="bar-wrap">'
                        f'<div class="bar-label">{k}: +{v}</div>'
                        f'<div class="bar-track">'
                        f'<div class="bar-fill" style="width:{width}%"></div>'
                        f'</div></div>'
                    )

                html = (
                    f'<div class="{card_class}">'
                    f'<h3>Item {aid}</h3>'
                    f'<p>Score <b>{round(score,2)}</b></p>'
                    f'{badge_html}'
                    f'{bars_html}'
                    f'</div>'
                )

                st.markdown(html, unsafe_allow_html=True)

                if st.button(f"Add {aid}", key=f"add_{aid}_{idx}"):
                    st.session_state.session_items.append(aid)
                    st.rerun()