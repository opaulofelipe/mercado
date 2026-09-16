import streamlit as st


PALETTE = {
    "green": "#9EE493",
    "mint": "#DAF7DC",
    "sage": "#ABC8C0",
    "mauve": "#70566D",
    "plum": "#42273B",
}


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
            :root {{
                --green: {PALETTE['green']};
                --mint: {PALETTE['mint']};
                --sage: {PALETTE['sage']};
                --mauve: {PALETTE['mauve']};
                --plum: {PALETTE['plum']};
                --bg: #080808;
                --surface: #1D1D1F;
                --surface-2: #242326;
                --text: #F3F2F4;
                --muted: #AAA5AC;
                --stroke: rgba(255,255,255,.055);
            }}

            html, body, [class*="css"] {{
                font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
            }}

            .stApp {{
                background: var(--bg);
                color: var(--text);
            }}

            header[data-testid="stHeader"] {{ background: transparent; }}
            #MainMenu, footer {{ visibility: hidden; }}

            .block-container {{
                max-width: 760px;
                padding: 1.3rem 1rem 2rem;
            }}

            .app-header {{
                padding: .2rem .15rem 1rem;
            }}

            .app-kicker {{
                color: var(--green);
                font-size: .88rem;
                font-weight: 700;
                margin-bottom: .22rem;
            }}

            .app-title {{
                color: var(--text);
                font-size: clamp(2rem, 7vw, 2.65rem);
                font-weight: 700;
                line-height: 1.05;
                letter-spacing: -.035em;
            }}

            .app-meta {{
                color: var(--muted);
                font-size: .92rem;
                margin-top: .42rem;
            }}

            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input,
            div[data-baseweb="select"] > div {{
                background: var(--surface) !important;
                color: var(--text) !important;
                border: 1px solid var(--stroke) !important;
                border-radius: 18px !important;
                min-height: 52px !important;
                box-shadow: none !important;
            }}

            div[data-testid="stTextInput"] input::placeholder {{
                color: #817C83 !important;
            }}

            div[data-testid="stVerticalBlockBorderWrapper"] {{
                background: var(--surface) !important;
                border: 1px solid var(--stroke) !important;
                border-radius: 20px !important;
                box-shadow: none !important;
                margin-bottom: .48rem;
            }}

            div[data-testid="stVerticalBlockBorderWrapper"] > div {{
                padding-top: .28rem;
                padding-bottom: .28rem;
            }}

            .task-name {{
                display: block;
                color: var(--text);
                font-size: 1.04rem;
                font-weight: 500;
                line-height: 1.2;
            }}

            .task-name.completed {{
                color: #969298;
                text-decoration: line-through;
                text-decoration-thickness: 1.5px;
            }}

            .task-meta {{
                display: block;
                color: #8D8890;
                font-size: .79rem;
                margin-top: .22rem;
            }}

            .task-copy-button {{
                background: transparent;
                border: 0;
                padding: .48rem .1rem .42rem;
                margin: 0;
                text-align: left;
                width: 100%;
                font: inherit;
            }}

            div[data-testid="stButton"] button,
            div[data-testid="stFormSubmitButton"] button {{
                min-height: 46px;
                border-radius: 17px;
                background: transparent;
                color: var(--muted);
                border: 0;
                box-shadow: none;
                font-weight: 600;
            }}

            div[data-testid="stButton"] button:hover,
            div[data-testid="stFormSubmitButton"] button:hover {{
                background: rgba(255,255,255,.045);
                color: var(--text);
                border: 0;
            }}

            div[data-testid="stFormSubmitButton"] button[kind="primary"] {{
                background: rgba(158,228,147,.14);
                color: var(--green);
                border: 1px solid rgba(158,228,147,.12);
            }}

            div[data-testid="stHorizontalBlock"] div[data-testid="column"]:first-child div[data-testid="stButton"] button {{
                font-size: 1.45rem;
                color: var(--sage);
            }}

            div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(3) div[data-testid="stButton"] button {{
                font-size: 1.3rem;
                color: #8E8A90;
            }}

            details {{
                background: transparent !important;
                border: 0 !important;
            }}

            details > summary {{
                width: fit-content;
                background: rgba(158,228,147,.13);
                color: #74C29D !important;
                border-radius: 14px;
                padding: .62rem .9rem !important;
                font-weight: 700;
                margin: .55rem 0 .5rem;
            }}

            details > div {{
                border: 0 !important;
                padding-left: 0 !important;
                padding-right: 0 !important;
            }}

            .edit-heading {{
                color: var(--green);
                font-size: .88rem;
                font-weight: 700;
                margin: .25rem 0 .65rem;
            }}

            label[data-testid="stWidgetLabel"] p {{
                color: var(--muted) !important;
                font-size: .82rem;
            }}

            .empty-state {{
                background: var(--surface);
                border: 1px solid var(--stroke);
                border-radius: 20px;
                padding: 1.8rem 1rem;
                margin-bottom: .65rem;
                text-align: center;
            }}

            .empty-title {{
                color: var(--text);
                font-weight: 650;
                font-size: 1rem;
            }}

            .empty-copy {{
                color: var(--muted);
                font-size: .86rem;
                margin-top: .25rem;
            }}

            .loading-state {{
                color: var(--muted);
                text-align: center;
                padding: 3rem 1rem;
            }}

            .add-spacer {{ height: .8rem; }}
            .bottom-safe-area {{ height: 2rem; }}

            @media (max-width: 640px) {{
                .block-container {{
                    max-width: 100%;
                    padding: .8rem .68rem 1.5rem;
                }}

                .app-header {{
                    padding-top: .2rem;
                    padding-bottom: .75rem;
                }}

                .app-title {{ font-size: 2rem; }}

                div[data-testid="stVerticalBlockBorderWrapper"] {{
                    border-radius: 18px !important;
                    margin-bottom: .4rem;
                }}

                div[data-testid="stTextInput"] input,
                div[data-testid="stNumberInput"] input,
                div[data-baseweb="select"] > div {{
                    min-height: 50px !important;
                }}

                div[data-testid="stButton"] button,
                div[data-testid="stFormSubmitButton"] button {{
                    min-height: 46px;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
