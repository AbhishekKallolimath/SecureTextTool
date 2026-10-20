
import streamlit as st

from crypto_engine import encrypt_text, decrypt_text


st.set_page_config(
    page_title="CipherDesk | Secure Text",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: #080d18;
        color: #e8eef8;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #0c1423;
        border-right: 1px solid #1c2a3e;
    }

    [data-testid="stSidebar"] * {
        color: #dce7f7;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .brand span { color: #a3ff70; }

    .muted {
        color: #8392aa;
        font-size: 13px;
    }

    .eyebrow {
        color: #a3ff70;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero {
        padding: 24px 0 18px 0;
    }

    .hero h1 {
        font-size: clamp(32px, 4vw, 48px);
        line-height: 1.1;
        letter-spacing: -2px;
        font-weight: 800;
        margin: 12px 0;
        color: #f1f5fb;
    }

    .hero h1 span { color: #a3ff70; }

    .panel {
        background: #101a2a;
        border: 1px solid #243249;
        border-radius: 16px;
        padding: 22px;
        margin: 8px 0 18px 0;
    }

    .panel-label {
        color: #94a5bd;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .status-dot {
        display: inline-block;
        height: 8px;
        width: 8px;
        border-radius: 50%;
        background: #a3ff70;
        margin-right: 8px;
        box-shadow: 0 0 10px #a3ff7060;
    }

    .metric {
        background: #101a2a;
        border: 1px solid #243249;
        border-radius: 12px;
        padding: 15px;
        min-height: 85px;
    }

    .metric-value {
        font-size: 18px;
        font-weight: 700;
        margin-top: 8px;
        color: #a3ff70;
    }

    .stTextArea textarea, .stTextInput input {
        background: #0a1220 !important;
        color: #f1f5fb !important;
        border: 1px solid #2b3b53 !important;
        border-radius: 10px !important;
        font-family: 'DM Mono', monospace !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #a3ff70 !important;
        box-shadow: 0 0 0 1px #a3ff70 !important;
    }

    .stButton > button, .stDownloadButton > button {
        background: #a3ff70;
        color: #0a1220;
        border: none;
        border-radius: 9px;
        font-weight: 800;
        min-height: 44px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #c0ff9d;
        color: #080d18;
        border: none;
        transform: translateY(-1px);
    }

    div[data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #243249;
    }

    button[data-baseweb="tab"] {
        color: #93a3ba;
        border-radius: 8px 8px 0 0;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #a3ff70;
        border-bottom-color: #a3ff70;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr { border-color: #243249; }

    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# Sidebar
with st.sidebar:
    st.markdown(
        '<div class="brand">CIPHER<span>DESK</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="muted">PERSONAL ENCRYPTION WORKSPACE</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("### Navigation")
    page = st.radio(
        "Choose workspace",
        ["Encrypt Message", "Decrypt Message", "About Security"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(
        """
        <div class="panel-label">CRYPTOGRAPHIC ENGINE</div>
        <br>
        <div><span class="status-dot"></span> AES-256-GCM</div>
        <br>
        <div><span class="status-dot"></span> Scrypt key derivation</div>
        <br>
        <div class="muted">Local application · Password-based encryption</div>
        """,
        unsafe_allow_html=True,
    )


# Header
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">SECURE COMMUNICATIONS / TOOLKIT 01</div>
        <h1>Your message.<br><span>Your control.</span></h1>
        <div class="muted">
            Encrypt private text, transport it safely, and decrypt it only
            with the correct password.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status and algorithm cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="metric"><div class="panel-label">ENCRYPTION</div>'
        '<div class="metric-value">AES-256-GCM</div></div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        '<div class="metric"><div class="panel-label">KEY DERIVATION</div>'
        '<div class="metric-value">SCRYPT</div></div>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        '<div class="metric"><div class="panel-label">INTEGRITY CHECK</div>'
        '<div class="metric-value">AUTHENTICATED</div></div>',
        unsafe_allow_html=True,
    )

st.write("")


if page == "Encrypt Message":
    st.markdown(
        '<div class="eyebrow">01 / ENCRYPTION WORKSPACE</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Convert plain text into protected data")
    st.markdown(
        '<div class="muted">Your message is encrypted in the application. '
        'A fresh salt and nonce are generated for every operation.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        message = st.text_area(
            "PLAINTEXT INPUT",
            placeholder="Type the message you want to protect...",
            height=180,
            key="plain_message",
        )

        password = st.text_input(
            "ENCRYPTION PASSWORD",
            type="password",
            placeholder="Enter a strong password",
            key="encrypt_password",
        )

        if st.button("ENCRYPT MESSAGE  →", use_container_width=True):
            if not message:
                st.error("Enter a message before encrypting.")
            elif len(password) < 12:
                st.error("Use a password with at least 12 characters.")
            else:
                try:
                    result = encrypt_text(message, password)
                    st.session_state["cipher_result"] = result
                    st.success("Encryption completed.")
                except Exception:
                    st.error("Encryption failed. Check your input and try again.")

    if st.session_state.get("cipher_result"):
        st.markdown("#### Encrypted payload")
        st.caption("Copy or download the complete encoded payload.")
        st.code(st.session_state["cipher_result"], language="text")
        st.download_button(
            "DOWNLOAD ENCRYPTED PAYLOAD",
            data=st.session_state["cipher_result"],
            file_name="ciphertext.txt",
            mime="text/plain",
            use_container_width=True,
        )


elif page == "Decrypt Message":
    st.markdown(
        '<div class="eyebrow">02 / DECRYPTION WORKSPACE</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Recover your original message")
    st.markdown(
        '<div class="muted">The encrypted payload and the original password '
        'are both required.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        encrypted_input = st.text_area(
            "ENCRYPTED PAYLOAD",
            placeholder="Paste the complete ciphertext here...",
            height=180,
            key="cipher_input",
        )

        password = st.text_input(
            "DECRYPTION PASSWORD",
            type="password",
            placeholder="Enter the original password",
            key="decrypt_password",
        )

        if st.button("DECRYPT MESSAGE  →", use_container_width=True):
            if not encrypted_input.strip() or not password:
                st.error("Provide both the encrypted payload and password.")
                st.session_state.pop("plain_result", None)
            else:
                try:
                    result = decrypt_text(encrypted_input.strip(), password)
                    st.session_state["plain_result"] = result
                    st.success("Authentication passed. Message recovered.")
                except ValueError as exc:
                    st.session_state.pop("plain_result", None)
                    st.error(str(exc))
                except Exception:
                    st.session_state.pop("plain_result", None)
                    st.error("Unable to decrypt this payload.")

    if "plain_result" in st.session_state:
        st.markdown("#### Recovered plaintext")
        st.text_area(
            "DECRYPTED MESSAGE",
            value=st.session_state["plain_result"],
            height=160,
            disabled=True,
        )
        st.download_button(
            "DOWNLOAD RECOVERED TEXT",
            data=st.session_state["plain_result"],
            file_name="decrypted_message.txt",
            mime="text/plain",
            use_container_width=True,
        )


else:
    st.markdown(
        '<div class="eyebrow">03 / SECURITY OVERVIEW</div>',
        unsafe_allow_html=True,
    )
    st.subheader("How CipherDesk protects your text")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-label">01 — CONFIDENTIALITY</div>
            <h3>AES-256-GCM</h3>
            Encrypts your message and authenticates the encrypted data.
            Modified ciphertext should not decrypt successfully.
        </div>
        <div class="panel">
            <div class="panel-label">02 — PASSWORD-BASED KEY</div>
            <h3>Scrypt</h3>
            Derives a 256-bit encryption key from your password and a random salt.
            This makes password guessing more computationally expensive.
        </div>
        <div class="panel">
            <div class="panel-label">03 — RANDOMNESS</div>
            <h3>Fresh salt and nonce</h3>
            Each encryption creates a new salt and nonce. The salt is used for
            key derivation; the nonce is used by AES-GCM.
        </div>
        <div class="panel">
            <div class="panel-label">IMPORTANT LIMITATION</div>
            Never share your password with the encrypted payload. This project
            is an educational application, not a professionally audited security
            product. Strong encryption cannot compensate for a weak password
            or an infected device.
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()
st.markdown(
    '<div class="muted">CIPHERDESK · SECURE TEXT TOOL · '
    'BUILT WITH PYTHON + STREAMLIT</div>',
    unsafe_allow_html=True,
)
