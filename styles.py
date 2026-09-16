import streamlit as st


PALETTE = {
    "green": "#9EE493",
    "mint": "#DAF7DC",
    "sage": "#ABC8C0",
    "mauve": "#70566D",
    "plum": "#42273B",
    "white": "#FFFFFF",
    "canvas": "#F6F7F6",
    "soft": "#F0F3F1",
}


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
            :root {{
                --green: {PALETTE["green"]};
                --mint: {PALETTE["mint"]};
                --sage: {PALETTE["sage"]};
                --mauve: {PALETTE["mauve"]};
                --plum: {PALETTE["plum"]};
                --white: {PALETTE["white"]};
                --canvas: {PALETTE["canvas"]};
                --soft: {PALETTE["soft"]};
            }}

            html, body, [class*="css"] {{
                font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
            }}

            .stApp {{
                background: var(--canvas);
                color: var(--plum);
            }}

            header[data-testid="stHeader"] {{
                background: transparent;
            }}

            #MainMenu, footer {{
                visibility: hidden;
            }}

            .block-container {{
                max-width: 900px;
                padding-top: 2.2rem;
                padding-bottom: 5rem;
            }}

            section[data-testid="stSidebar"] {{
                background: #F1F4F2;
                border-right: 1px solid rgba(171, 200, 192, .55);
            }}

            section[data-testid="stSidebar"] .block-container {{
                padding-top: 1.5rem;
            }}

            .brand {{
                color: var(--plum);
                font-size: 1.15rem;
                font-weight: 700;
                letter-spacing: -.02em;
                margin: .25rem 0 1.2rem;
            }}

            .page-title {{
                color: var(--plum);
                font-size: clamp(1.8rem, 4vw, 2.35rem);
                line-height: 1.15;
                letter-spacing: -.035em;
                font-weight: 700;
                margin: 0;
            }}

            .page-meta {{
                color: var(--mauve);
                font-size: .91rem;
                margin-top: .35rem;
                margin-bottom: 1.35rem;
            }}

            .list-label {{
                color: var(--mauve);
                font-size: .83rem;
                font-weight: 600;
                margin: 1.15rem 0 .45rem;
            }}

            .item-title {{
                color: var(--plum);
                font-size: 1rem;
                font-weight: 600;
                line-height: 1.3;
                margin-top: .08rem;
            }}

            .item-title.done {{
                text-decoration: line-through;
                color: var(--mauve);
                opacity: .78;
            }}

            .item-meta {{
                color: var(--mauve);
                font-size: .79rem;
                line-height: 1.35;
                margin-top: .18rem;
            }}

            .empty-state {{
                border: 1px dashed rgba(112, 86, 109, .35);
                border-radius: 10px;
                padding: 2.2rem 1rem;
                text-align: center;
                color: var(--mauve);
                background: rgba(255, 255, 255, .58);
                margin-top: 1rem;
            }}

            .empty-state strong {{
                color: var(--plum);
                display: block;
                margin-bottom: .2rem;
            }}

            div[data-testid="stForm"] {{
                background: transparent;
                border: 0;
                padding: 0;
            }}

            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input,
            div[data-baseweb="select"] > div {{
                border-radius: 8px !important;
                border-color: rgba(112, 86, 109, .22) !important;
                background: var(--white) !important;
                color: var(--plum) !important;
                min-height: 42px;
            }}

            div[data-testid="stTextInput"] input:focus,
            div[data-testid="stNumberInput"] input:focus {{
                border-color: var(--mauve) !important;
                box-shadow: 0 0 0 2px rgba(112, 86, 109, .14) !important;
            }}

            .add-caption {{
                color: var(--mauve);
                font-size: .82rem;
                margin-bottom: .4rem;
            }}

            div[data-testid="stButton"] button,
            div[data-testid="stFormSubmitButton"] button {{
                border-radius: 8px;
                min-height: 40px;
                font-weight: 600;
                box-shadow: none;
                transition: background .12s ease, border-color .12s ease, transform .12s ease;
            }}

            div[data-testid="stButton"] button:hover,
            div[data-testid="stFormSubmitButton"] button:hover {{
                transform: none;
            }}

            div[data-testid="stVerticalBlockBorderWrapper"] {{
                border: 1px solid rgba(171, 200, 192, .58) !important;
                border-radius: 9px !important;
                background: var(--white);
                box-shadow: none !important;
            }}

            div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
                border-color: rgba(112, 86, 109, .35) !important;
            }}

            details {{
                border-color: rgba(171, 200, 192, .55) !important;
                border-radius: 9px !important;
                background: transparent !important;
            }}

            div[data-testid="stCheckbox"] label {{
                min-height: 44px;
                align-items: center;
            }}

            section[data-testid="stSidebar"] div[role="radiogroup"] label {{
                min-height: 42px;
                border-radius: 8px;
                padding-left: .35rem;
            }}

            section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
                background: rgba(218, 247, 220, .72);
            }}

            label[data-testid="stWidgetLabel"] p {{
                color: var(--plum);
                font-weight: 600;
            }}

            @media (max-width: 700px) {{
                .block-container {{
                    padding: 1.15rem .9rem 4rem;
                }}

                .page-title {{
                    font-size: 1.85rem;
                }}

                .page-meta {{
                    margin-bottom: 1rem;
                }}

                div[data-testid="stHorizontalBlock"] {{
                    gap: .55rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
