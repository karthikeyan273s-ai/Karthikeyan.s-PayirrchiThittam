import base64
import html
import os
from pathlib import Path

import requests
import streamlit as st

from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


DEFAULT_LOGO = (
    Path(__file__).resolve()
    .parent.parent
    / "assets"
    / "logo.png"
)


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


st.markdown(
    """
<style>

.main-title {

    text-align: center;

    font-size: 2.6rem;

    font-weight: 800;

    margin-bottom: 0;
}

.subtitle {

    text-align: center;

    color: #6b7280;

    margin-bottom: 1.5rem;
}

.preview {

    background: #111827;

    color: #f9fafb;

    padding: 24px;

    border-radius: 14px;

    max-height: 620px;

    overflow-y: auto;

    line-height: 1.65;
}

.preview p {

    margin-bottom: 10px;
}

.notice {

    background: #fff7ed;

    padding: 12px 16px;

    border-left: 4px solid #f97316;

    border-radius: 8px;

    color: #7c2d12;
}

</style>
""",
    unsafe_allow_html=True
)


a, b, c = st.columns(
    [1, 2, 1]
)


with b:

    if DEFAULT_LOGO.exists():

        st.image(
            str(DEFAULT_LOGO),
            width=90
        )

    st.markdown(
        '<div class="main-title">'
        'LegalEase'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Powered Legal Document Generator'
        '</div>',
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="notice">'
    'AI-assisted drafts only. Review important '
    'documents with a qualified legal professional '
    'before signing or use.'
    '</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.header(
        "Document Settings"
    )

    document_type = st.selectbox(

        "Document type",

        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement (NDA)",
            "Freelance Work Contract",
            "Employment Offer Letter",
            "General Agreement",
            "Custom"
        ]
    )

    if document_type == "Custom":

        document_type = st.text_input(
            "Custom document type",
            "Service Agreement"
        )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Tamil"
        ]
    )

    tone = st.selectbox(

        "Tone",

        [
            "Formal and professional",
            "Simple and clear",
            "Detailed and formal"
        ]
    )

    logo_file = st.file_uploader(

        "Optional custom logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


st.subheader(
    "1. Enter document details"
)


left, right = st.columns(2)


with left:

    parties = st.text_area(

        "Parties involved",

        placeholder=(
            "Jane Doe (Service Provider); "
            "TechNova Inc. (Client)"
        ),

        height=130
    )

    dates = st.text_input(

        "Effective date",

        placeholder="October 10, 2026"
    )


with right:

    terms = st.text_area(

        "Terms & conditions",

        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),

        height=130
    )


if st.button(

    "Generate Document",

    type="primary",

    use_container_width=True
):

    if not all(
        x.strip()
        for x in [
            document_type,
            parties,
            terms,
            dates
        ]
    ):

        st.error(
            "Please complete document type, "
            "parties, terms, and effective date."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "dates":
                dates,

            "language":
                language,

            "tone":
                tone
        }

        try:

            with st.spinner(
                "Generating your legal draft..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=180
                )

            if response.ok:

                data = response.json()

                st.session_state.update(

                    document_text=data["text"],

                    document_type=document_type,

                    terms=terms,

                    effective_date=dates
                )

                st.success(
                    "Document generated successfully."
                )

            else:

                st.error(
                    response.json().get(
                        "detail",
                        response.text
                    )
                )

        except requests.RequestException as exc:

            st.error(
                f"Could not connect to FastAPI backend: {exc}"
            )


if "document_text" in st.session_state:

    st.divider()

    st.subheader(
        "2. Preview & edit"
    )

    edited = st.text_area(

        "Editable document",

        value=st.session_state[
            "document_text"
        ],

        height=520,

        label_visibility="collapsed"
    )

    st.session_state[
        "document_text"
    ] = edited

    safe = "<br>".join(

        html.escape(line)

        for line in edited.splitlines()
    )

    st.markdown(

        f'<div class="preview">'
        f'{safe}'
        f'</div>',

        unsafe_allow_html=True
    )

    st.subheader(
        "3. Download"
    )


    logo_b64 = None


    if logo_file:

        logo_b64 = (
            "data:image/png;base64,"
            + base64.b64encode(
                logo_file.getvalue()
            ).decode()
        )

    elif DEFAULT_LOGO.exists():

        logo_b64 = (
            "data:image/png;base64,"
            + base64.b64encode(
                DEFAULT_LOGO.read_bytes()
            ).decode()
        )


    export_payload = {

        "text":
            edited,

        "document_type":
            st.session_state[
                "document_type"
            ],

        "terms":
            st.session_state[
                "terms"
            ],

        "effective_date":
            st.session_state[
                "effective_date"
            ],

        "logo_base64":
            logo_b64
    }


    def download(

        endpoint,

        label,

        mime,

        filename
    ):

        try:

            response = requests.post(

                f"{BACKEND_URL}{endpoint}",

                json=export_payload,

                timeout=60
            )

            if response.ok:

                st.download_button(

                    label,

                    response.content,

                    file_name=filename,

                    mime=mime,

                    use_container_width=True
                )

            else:

                st.error(
                    response.text
                )

        except requests.RequestException as exc:

            st.error(
                f"Export failed: {exc}"
            )


    x, y, z = st.columns(3)


    with x:

        download(

            "/export/txt",

            "Download TXT",

            "text/plain",

            "legal_document.txt"
        )


    with y:

        download(

            "/export/docx",

            "Download DOCX",

            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

            "legal_document.docx"
        )


    with z:

        download(

            "/export/pdf",

            "Download PDF",

            "application/pdf",

            "legal_document.pdf"
        )


st.divider()


st.caption(

    "LegalEase • AI-assisted drafting • "
    "Verify facts, jurisdiction, and legal "
    "enforceability before use."
)