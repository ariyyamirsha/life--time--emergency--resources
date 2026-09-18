"""
Life Time Emergency Resources Finder
A single-page Streamlit application with a professional emergency-app UI.

Run with:
    streamlit run app.py
"""

import urllib.parse
import streamlit as st

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Life Time Emergency Resources Finder",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# DEMO DATA
# ----------------------------------------------------------------------------
HOSPITALS = [
    {"name": "Apollo Hospitals - Greams Road", "address": "21 Greams Lane, Off Greams Road, Chennai",
     "distance": 1.2, "status": "Open 24x7", "phone": "+914428293333"},
    {"name": "Fortis Malar Hospital", "address": "52 1st Main Road, Gandhi Nagar, Adyar, Chennai",
     "distance": 2.8, "status": "Open 24x7", "phone": "+914442892222"},
    {"name": "Government General Hospital", "address": "Park Town, Chennai",
     "distance": 4.5, "status": "Open 24x7", "phone": "+914425305000"},
    {"name": "MIOT International", "address": "4/112 Mount Poonamallee Road, Manapakkam, Chennai",
     "distance": 6.1, "status": "Open 24x7", "phone": "+914442002288"},
]

AMBULANCE = [
    {"name": "108 Government Emergency Ambulance", "address": "Tamil Nadu Emergency Services (State-wide)",
     "distance": 0.5, "status": "Available", "phone": "108"},
    {"name": "Apollo Ambulance Service", "address": "Greams Road, Chennai",
     "distance": 1.2, "status": "Available", "phone": "+914428293333"},
    {"name": "Ford Hospital Ambulance", "address": "Nungambakkam, Chennai",
     "distance": 3.0, "status": "Available", "phone": "+914443440000"},
]

BLOOD_BANKS = [
    {"name": "Government Blood Bank - Egmore", "address": "Egmore, Chennai",
     "distance": 3.4, "status": "Open", "phone": "+914428193000"},
    {"name": "Red Cross Blood Bank", "address": "Egmore, Chennai",
     "distance": 3.6, "status": "Open", "phone": "+914428192555"},
    {"name": "Lions Blood Bank", "address": "T Nagar, Chennai",
     "distance": 5.0, "status": "Closed", "phone": "+914424341234"},
]

PHARMACIES = [
    {"name": "Apollo Pharmacy - Adyar", "address": "Lattice Bridge Road, Adyar, Chennai",
     "distance": 1.0, "status": "Open 24x7", "phone": "+914424451122"},
    {"name": "MedPlus - Besant Nagar", "address": "Besant Nagar, Chennai",
     "distance": 2.1, "status": "Open", "phone": "+914424463344"},
    {"name": "Netmeds Pharmacy - T Nagar", "address": "T Nagar, Chennai",
     "distance": 4.0, "status": "Open", "phone": "+914428155566"},
]

POLICE = [
    {"name": "Adyar Police Station", "address": "Lattice Bridge Road, Adyar, Chennai",
     "distance": 1.5, "status": "Open 24x7", "phone": "100"},
    {"name": "T Nagar Police Station", "address": "T Nagar, Chennai",
     "distance": 4.2, "status": "Open 24x7", "phone": "100"},
]

FIRE = [
    {"name": "Adyar Fire Station", "address": "Adyar, Chennai",
     "distance": 2.0, "status": "Open 24x7", "phone": "101"},
    {"name": "Chennai Central Fire Station", "address": "Park Town, Chennai",
     "distance": 5.5, "status": "Open 24x7", "phone": "101"},
]

CATEGORIES = {
    "Hospitals":       {"icon": "🏥", "data": HOSPITALS,    "color": "#E63946"},
    "Ambulance":       {"icon": "🚑", "data": AMBULANCE,    "color": "#F4A261"},
    "Blood Banks":     {"icon": "🩸", "data": BLOOD_BANKS,  "color": "#D00000"},
    "Pharmacies":      {"icon": "💊", "data": PHARMACIES,   "color": "#2A9D8F"},
    "Police Stations": {"icon": "👮", "data": POLICE,       "color": "#1D3557"},
    "Fire Stations":   {"icon": "🚒", "data": FIRE,         "color": "#E76F51"},
}

EMERGENCY_NUMBERS = [
    {"label": "Ambulance", "number": "108", "icon": "🚑"},
    {"label": "Police", "number": "100", "icon": "👮"},
    {"label": "Fire", "number": "101", "icon": "🚒"},
    {"label": "Women's Helpline", "number": "1091", "icon": "🆘"},
]

# ----------------------------------------------------------------------------
# SESSION STATE (router)
# ----------------------------------------------------------------------------
defaults = {
    "page": "home",
    "active_category": "Hospitals",
    "search_query": "",
    "selected_resource": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go_to(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v


# ----------------------------------------------------------------------------
# STYLES
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}
.block-container { padding-top: 1rem; padding-bottom: 4rem; max-width: 1100px; }

:root {
    --navy: #1D3557;
    --red: #E63946;
    --teal: #2A9D8F;
    --bg: #F6F8FB;
    --card: #FFFFFF;
    --muted: #6B7280;
}

/* App shell background */
.stApp { background-color: var(--bg); }

/* Top brand header */
.app-header {
    background: linear-gradient(135deg, var(--navy) 0%, #274472 100%);
    border-radius: 20px;
    padding: 28px 32px;
    color: white;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(29,53,87,0.25);
}
.app-header h1 { margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }
.app-header p { margin: 6px 0 0 0; font-size: 15px; opacity: 0.85; font-weight: 400; }

/* Sticky nav */
.nav-wrap { position: sticky; top: 0; z-index: 999; background: var(--bg); padding: 6px 0 12px 0; }

/* Cards */
.res-card {
    background: var(--card);
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(16,24,40,0.06);
    border: 1px solid #EEF1F5;
}
.res-card h4 { margin: 0 0 4px 0; color: var(--navy); font-size: 17px; font-weight: 700; }
.res-card .addr { color: var(--muted); font-size: 13.5px; margin-bottom: 8px; }
.badge {
    display: inline-block; padding: 3px 11px; border-radius: 20px;
    font-size: 12px; font-weight: 600; margin-right: 8px;
}
.badge-open { background: #E7F7F1; color: #0F9D6E; }
.badge-closed { background: #FDECEC; color: #D64545; }
.badge-dist { background: #EEF2FF; color: #3B4FBF; }

.cat-card {
    background: var(--card);
    border-radius: 18px;
    padding: 20px 14px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(16,24,40,0.06);
    border: 1px solid #EEF1F5;
    height: 100%;
}
.cat-card .icon { font-size: 34px; }
.cat-card .label { font-weight: 700; color: var(--navy); font-size: 14.5px; margin-top: 6px; }

.sos-banner {
    background: linear-gradient(135deg, #E63946 0%, #C1121F 100%);
    border-radius: 20px;
    padding: 22px 26px;
    color: white;
    box-shadow: 0 10px 26px rgba(230,57,70,0.35);
    margin-bottom: 18px;
}
.sos-banner h3 { margin: 0; font-size: 20px; font-weight: 800; }
.sos-banner p { margin: 4px 0 0 0; font-size: 13.5px; opacity: 0.9; }

.section-title { color: var(--navy); font-weight: 800; font-size: 19px; margin: 18px 0 10px 0; }

.detail-hero {
    background: var(--card);
    border-radius: 20px;
    padding: 26px 28px;
    box-shadow: 0 4px 18px rgba(16,24,40,0.08);
    border: 1px solid #EEF1F5;
    margin-bottom: 16px;
}
.detail-hero h2 { color: var(--navy); margin: 0 0 6px 0; }
.detail-row { display:flex; gap:10px; align-items:center; margin: 6px 0; color:#374151; font-size:15px; }

.profile-card {
    background: var(--card); border-radius: 18px; padding: 22px;
    box-shadow: 0 2px 10px rgba(16,24,40,0.06); border: 1px solid #EEF1F5;
}

/* Buttons */
div.stButton > button, .stLinkButton > a {
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border: none !important;
}
div.stButton > button[kind="primary"] { background-color: var(--navy) !important; }

/* Nav buttons */
.navbtn button {
    width: 100%;
    background: var(--card) !important;
    color: var(--navy) !important;
    border: 1px solid #E5E9F0 !important;
    font-weight: 600 !important;
}
.navbtn-active button {
    background: var(--navy) !important;
    color: white !important;
    border: 1px solid var(--navy) !important;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def status_badge(status):
    cls = "badge-open" if status.lower().startswith("open") or status.lower() == "available" else "badge-closed"
    return f'<span class="badge {cls}">{status}</span>'


def maps_url(address):
    q = urllib.parse.quote(address)
    return f"https://www.google.com/maps/search/?api=1&query={q}"


def render_resource_card(category, res, idx):
    with st.container():
        st.markdown(f"""
        <div class="res-card">
            <h4>{CATEGORIES[category]['icon']} {res['name']}</h4>
            <div class="addr">📍 {res['address']}</div>
            {status_badge(res['status'])}
            <span class="badge badge-dist">📏 {res['distance']} km away</span>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("View Details", key=f"view_{category}_{idx}", use_container_width=True):
                go_to("detail", selected_resource=(category, idx))
                st.rerun()
        with c2:
            st.link_button("📞 Call Now", f"tel:{res['phone']}", use_container_width=True)


# ----------------------------------------------------------------------------
# NAV BAR
# ----------------------------------------------------------------------------
def render_nav():
    st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)
    nav_items = [
        ("home", "🏠 Home"),
        ("find", "🔍 Find Resources"),
        ("nearby", "📍 Nearby"),
        ("emergency", "🚨 Emergency"),
        ("profile", "👤 Profile"),
    ]
    cols = st.columns(len(nav_items))
    for col, (key, label) in zip(cols, nav_items):
        active = st.session_state.page == key or (key == "find" and st.session_state.page == "detail")
        with col:
            st.markdown(f'<div class="navbtn{"-active" if active else ""}">', unsafe_allow_html=True)
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                go_to(key)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# SCREENS
# ----------------------------------------------------------------------------
def screen_home():
    st.markdown("""
    <div class="app-header">
        <h1>🚑 Life Time Emergency Resources Finder</h1>
        <p>Find Emergency Resources Quickly, Anytime.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sos-banner">
        <h3>🚨 In an emergency, tap SOS for instant help</h3>
        <p>One tap connects you to ambulance, police and fire services.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚨 SOS — Emergency Help", use_container_width=True, type="primary"):
            go_to("emergency")
            st.rerun()
    with c2:
        if st.button("🔍 Find Nearby Resources", use_container_width=True):
            go_to("find")
            st.rerun()

    st.markdown('<div class="section-title">Browse by Category</div>', unsafe_allow_html=True)
    cat_names = list(CATEGORIES.keys())
    cols = st.columns(3)
    for i, name in enumerate(cat_names):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="cat-card">
                <div class="icon">{CATEGORIES[name]['icon']}</div>
                <div class="label">{name}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open", key=f"home_cat_{name}", use_container_width=True):
                go_to("find", active_category=name, search_query="")
                st.rerun()
            st.write("")


def screen_find():
    st.markdown('<div class="section-title">🔍 Find Emergency Resources</div>', unsafe_allow_html=True)

    st.session_state.search_query = st.text_input(
        "Search", value=st.session_state.search_query,
        placeholder="Search by name or area (e.g. 'Adyar', 'Apollo')...",
        label_visibility="collapsed",
    )

    chip_cols = st.columns(len(CATEGORIES))
    for col, name in zip(chip_cols, CATEGORIES.keys()):
        with col:
            active = st.session_state.active_category == name
            st.markdown(f'<div class="navbtn{"-active" if active else ""}">', unsafe_allow_html=True)
            if st.button(f"{CATEGORIES[name]['icon']} {name}", key=f"chip_{name}", use_container_width=True):
                st.session_state.active_category = name
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    cat = st.session_state.active_category
    results = CATEGORIES[cat]["data"]
    q = st.session_state.search_query.strip().lower()
    if q:
        results = [r for r in results if q in r["name"].lower() or q in r["address"].lower()]
    results = sorted(results, key=lambda r: r["distance"])

    st.caption(f"{len(results)} result(s) found near you")
    if not results:
        st.info("No resources match your search. Try a different keyword or category.")
    for idx, res in enumerate(results):
        real_idx = CATEGORIES[cat]["data"].index(res)
        render_resource_card(cat, res, real_idx)


def screen_nearby():
    st.markdown('<div class="section-title">📍 All Nearby Resources</div>', unsafe_allow_html=True)
    st.caption("Sorted by distance across all emergency categories")
    all_res = []
    for cat, info in CATEGORIES.items():
        for idx, r in enumerate(info["data"]):
            all_res.append((cat, idx, r))
    all_res.sort(key=lambda t: t[2]["distance"])
    for cat, idx, res in all_res[:8]:
        render_resource_card(cat, res, idx)


def screen_detail():
    sel = st.session_state.selected_resource
    if not sel:
        st.info("No resource selected.")
        if st.button("⬅ Back to Find Resources"):
            go_to("find")
            st.rerun()
        return
    category, idx = sel
    res = CATEGORIES[category]["data"][idx]

    if st.button("⬅ Back"):
        go_to("find")
        st.rerun()

    st.markdown(f"""
    <div class="detail-hero">
        <h2>{CATEGORIES[category]['icon']} {res['name']}</h2>
        {status_badge(res['status'])}
        <span class="badge badge-dist">📏 {res['distance']} km away</span>
        <div class="detail-row">📍 <b>Address:</b> {res['address']}</div>
        <div class="detail-row">📞 <b>Phone:</b> {res['phone']}</div>
        <div class="detail-row">🏷️ <b>Category:</b> {category}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📞 Call Now", f"tel:{res['phone']}", use_container_width=True)
    with c2:
        st.link_button("🧭 Get Directions", maps_url(res["address"]), use_container_width=True)


def screen_emergency():
    st.markdown("""
    <div class="sos-banner">
        <h3>🚨 Emergency Assistance</h3>
        <p>Tap a number below to call immediately. No extra steps.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, item in enumerate(EMERGENCY_NUMBERS):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="res-card" style="text-align:center;">
                <div style="font-size:34px;">{item['icon']}</div>
                <h4>{item['label']}</h4>
                <div class="addr">Dial {item['number']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(f"📞 Call {item['number']}", f"tel:{item['number']}", use_container_width=True)
            st.write("")

    st.markdown('<div class="section-title">🏥 Nearest Hospital</div>', unsafe_allow_html=True)
    nearest = sorted(HOSPITALS, key=lambda r: r["distance"])[0]
    render_resource_card("Hospitals", nearest, HOSPITALS.index(nearest))


def screen_profile():
    st.markdown('<div class="section-title">👤 Profile</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="profile-card">
        <h3 style="color:#1D3557; margin-top:0;">Demo User</h3>
        <p style="color:#6B7280; margin:2px 0;">📧 demo.user@example.com</p>
        <p style="color:#6B7280; margin:2px 0;">📍 Chennai, Tamil Nadu, India</p>
        <p style="color:#6B7280; margin:2px 0;">🩸 Blood Group: O+</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Saved Emergency Contacts</div>', unsafe_allow_html=True)
    contacts = [
        {"name": "Home Emergency Contact", "phone": "+91 98765 43210"},
        {"name": "Family Doctor", "phone": "+91 91234 56789"},
    ]
    for c in contacts:
        st.markdown(f"""
        <div class="res-card">
            <h4>👤 {c['name']}</h4>
            <div class="addr">📞 {c['phone']}</div>
        </div>
        """, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# ROUTER
# ----------------------------------------------------------------------------
render_nav()

page = st.session_state.page
if page == "home":
    screen_home()
elif page == "find":
    screen_find()
elif page == "nearby":
    screen_nearby()
elif page == "detail":
    screen_detail()
elif page == "emergency":
    screen_emergency()
elif page == "profile":
    screen_profile()
else:
    screen_home()
