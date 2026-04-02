import streamlit as st
import pickle
import os
import gdown

# ================= CONFIG =================
st.set_page_config(page_title="RecoAI", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #0f172a);
    color: #e2e8f0;
}
.card {
    background: rgba(15, 23, 42, 0.85);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}
.top-card {
    border: 1px solid gold;
    box-shadow: 0 0 20px rgba(255,215,0,0.4);
}
.badge {padding:4px 10px;margin:4px;border-radius:20px;font-size:11px;}
.session {background:#064e3b;color:#34d399;}
.next {background:#0c4a6e;color:#38bdf8;}
.co {background:#312e81;color:#818cf8;}
.pop {background:#78350f;color:#fbbf24;}
.bar-track {width:100%;height:6px;background:#1e293b;border-radius:10px;}
.bar-fill {height:100%;background:linear-gradient(90deg,#22c55e,#3b82f6);}
</style>
""", unsafe_allow_html=True)

# ================= SAFE DOWNLOAD =================
def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        try:
            gdown.download(url, output, quiet=False, fuzzy=True)
        except:
            st.error(f"❌ Failed to download {output}")
            st.stop()

# ================= LOAD =================
@st.cache_resource
def load_data():

    download_file("1kX-7IOcW3c3LMrS_mjNMdrqj5KrkG8aG", "cooccur.pkl")
    download_file("1zpNURRMmhDsRHAJJw7XHKA6U4kgVlh4u", "next_top.pkl")
    download_file("1_uPDn5TtGttVZf-71NwvVOmAKVAcU6-N", "popular.pkl")

    cooccur = pickle.load(open("cooccur.pkl", "rb"))
    cooccur = dict(list(cooccur.items())[:20000])  # 🔥 reduced for cloud

    next_top = pickle.load(open("next_top.pkl", "rb"))
    popular_items = pickle.load(open("popular.pkl", "rb"))

    return cooccur, next_top, popular_items

cooccur, next_top, popular_items = load_data()

# ================= SESSION =================
if "session_items" not in st.session_state:
    st.session_state.session_items = []

# ================= MODEL =================
def recommend(session_items, k=5):
    if not session_items:
        return []

    results = []
    last_item = session_items[-1]
    session_set = set(session_items)

    candidates = set(popular_items[:100]) | session_set  # 🔥 lighter

    for aid in candidates:
        score = 0
        exp = {}

        if aid in session_set:
            score += 5; exp["Session"] = 5

        if last_item in next_top and aid in next_top[last_item]:
            score += 3; exp["Next"] = 3

        if cooccur:
            co_score = sum(
                2 for item in session_items
                if item in cooccur and aid in cooccur.get(item, {})
            )
        else:
            co_score = 0

        if co_score > 0:
            score += co_score; exp["Co"] = co_score

        if aid in popular_items[:100]:
            score += 1; exp["Popular"] = 1

        if score > 0:
            results.append((aid, score, exp))

    return sorted(results, key=lambda x: x[1], reverse=True)[:k]

# ================= UI =================
st.title("🛍️ RecoAI — Smart Recommender")

col1, col2 = st.columns([1, 3])

# LEFT PANEL
with col1:
    st.subheader("Session")

    new_item = st.text_input("Item ID")

    if st.button("Add"):
        if new_item.isdigit():
            st.session_state.session_items.append(int(new_item))

    if st.button("Clear"):
        st.session_state.session_items = []

    for i, item in enumerate(st.session_state.session_items):
        c1, c2 = st.columns([3,1])
        c1.write(f"Item {item}")
        if c2.button("❌", key=f"remove_{i}"):
            st.session_state.session_items.pop(i)
            st.rerun()

# RIGHT PANEL
with col2:
    if not st.session_state.session_items:
        st.info("Add items to start")
    else:
        recs = recommend(st.session_state.session_items)

        for idx, (aid, score, exp) in enumerate(recs):

            card_class = "card top-card" if idx == 0 else "card"

            badge_html = "".join([f'<span class="badge">{k}</span>' for k in exp])

            bars_html = "".join([
                f'<div>{k}: +{v}</div><div class="bar-track"><div class="bar-fill" style="width:{v*20}%"></div></div>'
                for k, v in exp.items()
            ])

            st.markdown(f"""
            <div class="{card_class}">
                <h3>Item {aid}</h3>
                <p>Score {round(score,2)}</p>
                {badge_html}
                {bars_html}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Add {aid}", key=f"add_{aid}_{idx}"):
                st.session_state.session_items.append(aid)
                st.rerun()