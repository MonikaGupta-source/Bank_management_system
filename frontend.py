import json
import random
import string
from pathlib import Path
from datetime import datetime
import streamlit as st

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeoBank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

    html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

    .stApp { background: #050507; }

    /* Animated grid background */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(0,255,180,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,180,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    h1,h2,h3 { color: #00ffb4 !important; font-family: 'Syne', sans-serif !important; }

    .bank-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(135deg, #00ffb4, #00b4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    .subtitle { color: #444; font-size: 0.9rem; margin-bottom: 2rem; font-family: 'Space Mono', monospace; }

    .card {
        background: #0d0d0f;
        border: 1px solid #1a1a1f;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00ffb4, #00b4ff);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .card:hover { border-color: #00ffb4; }
    .card:hover::before { opacity: 1; }

    .card-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e0e0e0;
        margin-bottom: 0.3rem;
    }
    .card-meta {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #444;
    }
    .balance-big {
        font-family: 'Space Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00ffb4;
    }

    .stat-box {
        background: #0d0d0f;
        border: 1px solid #1a1a1f;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-num {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        color: #00ffb4;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.72rem;
        color: #444;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'Space Mono', monospace;
    }
    .badge-green { background: #001f14; color: #00ffb4; border: 1px solid #00ffb430; }
    .badge-blue  { background: #001020; color: #00b4ff; border: 1px solid #00b4ff30; }
    .badge-red   { background: #1f0000; color: #ff4444; border: 1px solid #ff444430; }

    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ffb4;
        border-bottom: 1px solid #1a1a1f;
        padding-bottom: 0.5rem;
        margin-bottom: 1.2rem;
        font-family: 'Syne', sans-serif;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #0d0d0f !important;
        border: 1px solid #1a1a1f !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
        font-family: 'Space Mono', monospace !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #00ffb4 !important;
        box-shadow: 0 0 0 2px #00ffb420 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ffb4, #00b4ff) !important;
        color: #050507 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.8rem !important;
        font-family: 'Syne', sans-serif !important;
        letter-spacing: 0.5px !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }
    .stButton > button:disabled {
        background: #1a1a1f !important;
        color: #333 !important;
    }

    /* Sidebar */
    div[data-testid="stSidebar"] > div {
        background: #080809;
        border-right: 1px solid #1a1a1f;
    }

    label { color: #666 !important; font-size: 0.82rem !important; font-family: 'Space Mono', monospace !important; }

    .acc-number {
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        color: #00b4ff;
        background: #001020;
        padding: 2px 8px;
        border-radius: 6px;
    }

    hr { border-color: #1a1a1f !important; }

    /* Alert override */
    .stAlert { background: #0d0d0f !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Data Layer ────────────────────────────────────────────────────────────────
DATABASE = "bank_data.json"


def load_data():
    p = Path(DATABASE)
    if p.exists():
        content = p.read_text().strip()
        if content:
            return json.loads(content)
    return []


def save_data(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))


def gen_acc_num():
    alpha = random.choices(string.ascii_uppercase, k=3)
    nums = random.choices(string.digits, k=4)
    combo = alpha + nums
    random.shuffle(combo)
    return "ACC-" + "".join(combo)


def find_user(acc_num, pin, data):
    matches = [u for u in data if u["account_no"] == acc_num and u["pin"] == int(pin)]
    return matches[0] if matches else None


# ─── Session State ─────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "toast_msg" not in st.session_state:
    st.session_state.toast_msg = None
if "logged_in_acc" not in st.session_state:
    st.session_state.logged_in_acc = None

data = st.session_state.data

if st.session_state.toast_msg:
    st.toast(st.session_state.toast_msg, icon="✅")
    st.session_state.toast_msg = None

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="bank-title">NEO<br>BANK</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// next-gen banking</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "nav",
        ["🏠 Dashboard", "🆕 Create Account", "🔐 My Account", "💸 Deposit", "💳 Withdraw", "✏️ Update Details", "🗑️ Delete Account"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    total_accounts = len(data)
    total_balance = sum(u.get("balance", 0) for u in data)
    st.markdown(f'<div class="stat-box"><div class="stat-num">{total_accounts}</div><div class="stat-label">Accounts</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="stat-box"><div class="stat-num">₹{total_balance:,}</div><div class="stat-label">Total Deposits</div></div>', unsafe_allow_html=True)

# ─── Login helper ──────────────────────────────────────────────────────────────
def login_form(key_prefix):
    col1, col2 = st.columns(2)
    with col1:
        acc = st.text_input("Account Number", placeholder="ACC-XXXXXXX", key=f"{key_prefix}_acc")
    with col2:
        pin = st.text_input("PIN", type="password", max_chars=4, key=f"{key_prefix}_pin")
    return acc, pin

# ─── Dashboard ─────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown('<div class="bank-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// system overview</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{len(data)}</div><div class="stat-label">Total Accounts</div></div>', unsafe_allow_html=True)
    with c2:
        total_bal = sum(u.get("balance", 0) for u in data)
        st.markdown(f'<div class="stat-box"><div class="stat-num">₹{total_bal:,}</div><div class="stat-label">Total Balance</div></div>', unsafe_allow_html=True)
    with c3:
        avg_bal = int(total_bal / len(data)) if data else 0
        st.markdown(f'<div class="stat-box"><div class="stat-num">₹{avg_bal:,}</div><div class="stat-label">Avg Balance</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">All Accounts</div>', unsafe_allow_html=True)

    if not data:
        st.info("No accounts created yet.")
    else:
        search = st.text_input("🔍 Search by name or account number", placeholder="e.g. Rahul or ACC-...")
        filtered = data
        if search:
            filtered = [u for u in data if search.lower() in u["name"].lower() or search.lower() in u["account_no"].lower()]

        for u in filtered:
            bal = u.get("balance", 0)
            badge = f'<span class="badge badge-green">₹{bal:,}</span>'
            st.markdown(f'''
            <div class="card">
                <div class="card-name">{u["name"]} &nbsp; <span class="acc-number">{u["account_no"]}</span></div>
                <div class="card-meta">📧 {u["email"]} &nbsp;·&nbsp; 🎂 Age {u["age"]} &nbsp;·&nbsp; Balance: {badge}</div>
            </div>''', unsafe_allow_html=True)

# ─── Create Account ────────────────────────────────────────────────────────────
elif page == "🆕 Create Account":
    st.markdown('<div class="bank-title">Create Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// join neobank</div>', unsafe_allow_html=True)

    with st.form("create_acc"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            email = st.text_input("Email", placeholder="rahul@email.com")
        with col2:
            age = st.number_input("Age", min_value=1, max_value=120, value=18)
            pin = st.text_input("4-digit PIN", placeholder="e.g. 1234", type="password", max_chars=4)

        submitted = st.form_submit_button("🚀 Open Account")
        if submitted:
            if not name or not email or not pin:
                st.error("❌ Please fill all fields.")
            elif age < 18:
                st.error("❌ You must be 18+ to open an account.")
            elif not pin.isdigit() or len(pin) != 4:
                st.error("❌ PIN must be exactly 4 digits.")
            else:
                acc_no = gen_acc_num()
                new_user = {
                    "name": name,
                    "age": int(age),
                    "email": email,
                    "pin": int(pin),
                    "account_no": acc_no,
                    "balance": 0,
                    "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(new_user)
                save_data(data)
                st.session_state.toast_msg = f"Account created for {name}!"
                st.markdown(f'''
                <div class="card">
                    <div class="card-name">🎉 Account Created Successfully!</div>
                    <div class="card-meta" style="margin-top:0.5rem">
                        <b style="color:#e0e0e0">Name:</b> {name}<br>
                        <b style="color:#e0e0e0">Account No:</b> <span class="acc-number">{acc_no}</span><br>
                        <b style="color:#e0e0e0">Email:</b> {email}<br>
                        <b style="color:#e0e0e0">Age:</b> {age}<br>
                        <b style="color:#e0e0e0">Balance:</b> ₹0
                    </div>
                </div>''', unsafe_allow_html=True)
                st.warning("⚠️ Please note down your Account Number carefully!")
                st.rerun()

# ─── My Account ───────────────────────────────────────────────────────────────
elif page == "🔐 My Account":
    st.markdown('<div class="bank-title">My Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// view your details</div>', unsafe_allow_html=True)

    acc, pin = login_form("view")
    if st.button("🔍 View Details"):
        if not acc or not pin:
            st.error("Please enter account number and PIN.")
        else:
            user = find_user(acc, pin, data)
            if not user:
                st.error("❌ Invalid account number or PIN.")
            else:
                bal = user.get("balance", 0)
                st.markdown(f'''
                <div class="card">
                    <div class="card-name">{user["name"]}</div>
                    <div class="balance-big">₹{bal:,}</div>
                    <hr style="border-color:#1a1a1f; margin: 0.8rem 0;">
                    <div class="card-meta">
                        🆔 <span class="acc-number">{user["account_no"]}</span><br><br>
                        📧 {user["email"]}<br>
                        🎂 Age: {user["age"]}<br>
                        📅 Joined: {user.get("created_on", "N/A")}
                    </div>
                </div>''', unsafe_allow_html=True)

# ─── Deposit ───────────────────────────────────────────────────────────────────
elif page == "💸 Deposit":
    st.markdown('<div class="bank-title">Deposit</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// add funds to your account</div>', unsafe_allow_html=True)

    with st.form("deposit_form"):
        acc, pin = login_form("dep")
        amount = st.number_input("Amount to Deposit (max ₹10,000)", min_value=1, max_value=10000, value=100)
        submitted = st.form_submit_button("💸 Deposit Money")
        if submitted:
            if not acc or not pin:
                st.error("Please enter account number and PIN.")
            else:
                user = find_user(acc, pin, data)
                if not user:
                    st.error("❌ Invalid account number or PIN.")
                elif amount <= 0 or amount > 10000:
                    st.error("❌ Amount must be between ₹1 and ₹10,000.")
                else:
                    user["balance"] += amount
                    save_data(data)
                    st.session_state.toast_msg = f"₹{amount:,} deposited successfully!"
                    st.rerun()

# ─── Withdraw ──────────────────────────────────────────────────────────────────
elif page == "💳 Withdraw":
    st.markdown('<div class="bank-title">Withdraw</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// take out your funds</div>', unsafe_allow_html=True)

    with st.form("withdraw_form"):
        acc, pin = login_form("wd")
        amount = st.number_input("Amount to Withdraw", min_value=1, value=100)
        submitted = st.form_submit_button("💳 Withdraw Money")
        if submitted:
            if not acc or not pin:
                st.error("Please fill all fields.")
            else:
                user = find_user(acc, pin, data)
                if not user:
                    st.error("❌ Invalid account number or PIN.")
                elif amount <= 0:
                    st.error("❌ Invalid amount.")
                elif user["balance"] < amount:
                    st.error(f"❌ Insufficient balance. Available: ₹{user['balance']:,}")
                elif user["balance"] == amount:
                    st.error("❌ Cannot withdraw full balance. Account would be empty.")
                else:
                    user["balance"] -= amount
                    save_data(data)
                    st.session_state.toast_msg = f"₹{amount:,} withdrawn successfully!"
                    st.rerun()

# ─── Update Details ────────────────────────────────────────────────────────────
elif page == "✏️ Update Details":
    st.markdown('<div class="bank-title">Update Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// modify your info</div>', unsafe_allow_html=True)

    acc = st.text_input("Account Number", placeholder="ACC-XXXXXXX", key="upd_acc")
    pin = st.text_input("PIN", type="password", max_chars=4, key="upd_pin")

    if st.button("🔓 Load My Details"):
        user = find_user(acc, pin, data)
        if not user:
            st.error("❌ Invalid account number or PIN.")
        else:
            st.session_state.loaded_user_acc = acc
            st.session_state.loaded_user_pin = int(pin)

    if "loaded_user_acc" in st.session_state:
        user = find_user(st.session_state.loaded_user_acc, st.session_state.loaded_user_pin, data)
        if user:
            st.markdown('<div class="section-header">Edit Info</div>', unsafe_allow_html=True)
            st.info("Leave a field blank to keep it unchanged. Age, Account No, and Balance cannot be changed.")
            with st.form("update_form"):
                new_name = st.text_input("New Name", placeholder=user["name"])
                new_email = st.text_input("New Email", placeholder=user["email"])
                new_pin = st.text_input("New PIN", type="password", max_chars=4, placeholder="Leave blank to keep")
                submitted = st.form_submit_button("💾 Save Changes")
                if submitted:
                    changed = False
                    if new_name.strip():
                        user["name"] = new_name.strip()
                        changed = True
                    if new_email.strip():
                        user["email"] = new_email.strip()
                        changed = True
                    if new_pin.strip():
                        if new_pin.isdigit() and len(new_pin) == 4:
                            user["pin"] = int(new_pin)
                            changed = True
                        else:
                            st.error("❌ PIN must be 4 digits.")
                    if changed:
                        save_data(data)
                        del st.session_state.loaded_user_acc
                        del st.session_state.loaded_user_pin
                        st.session_state.toast_msg = "Details updated successfully!"
                        st.rerun()
                    else:
                        st.warning("No changes made.")

# ─── Delete Account ────────────────────────────────────────────────────────────
elif page == "🗑️ Delete Account":
    st.markdown('<div class="bank-title">Delete Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">// close your account permanently</div>', unsafe_allow_html=True)

    st.error("⚠️ This action is permanent and cannot be undone.")

    with st.form("delete_form"):
        acc, pin = login_form("del")
        confirm = st.checkbox("I understand this will permanently delete my account")
        submitted = st.form_submit_button("🗑️ Delete My Account")
        if submitted:
            if not acc or not pin:
                st.error("Please fill all fields.")
            elif not confirm:
                st.error("❌ Please confirm that you want to delete your account.")
            else:
                user = find_user(acc, pin, data)
                if not user:
                    st.error("❌ Invalid account number or PIN.")
                else:
                    name = user["name"]
                    data.remove(user)
                    save_data(data)
                    st.session_state.toast_msg = f"Account of {name} deleted."
                    st.rerun()