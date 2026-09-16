import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Mercado",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_PATH = Path(__file__).with_name("mercado.db")

COLORS = {
    "green": "#9EE493",
    "mint": "#DAF7DC",
    "sage": "#ABC8C0",
    "mauve": "#70566D",
    "plum": "#42273B",
    "bg": "#F6F7F8",
    "text": "#252229",
    "muted": "#77727A",
    "border": "#E7E5E8",
}

CATEGORIES = [
    "Geral",
    "Hortifruti",
    "Padaria",
    "Açougue",
    "Laticínios",
    "Mercearia",
    "Bebidas",
    "Higiene",
    "Limpeza",
    "Outros",
]

UNITS = ["un", "kg", "g", "L", "mL", "pct", "cx", "dz"]


st.markdown(
    f"""
    <style>
    :root {{
        --green: {COLORS['green']};
        --mint: {COLORS['mint']};
        --sage: {COLORS['sage']};
        --mauve: {COLORS['mauve']};
        --plum: {COLORS['plum']};
        --bg: {COLORS['bg']};
        --text: {COLORS['text']};
        --muted: {COLORS['muted']};
        --border: {COLORS['border']};
    }}

    html, body, [class*="css"] {{
        font-family: Inter, "Segoe UI", Arial, sans-serif;
    }}

    .stApp {{
        background: var(--bg);
        color: var(--text);
    }}

    .block-container {{
        max-width: 920px;
        padding-top: 2.1rem;
        padding-bottom: 5rem;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    section[data-testid="stSidebar"] {{
        background: #F1F5F3;
        border-right: 1px solid #E2E8E5;
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1.2rem;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: .65rem;
        margin-bottom: 1.4rem;
    }}

    .brand-icon {{
        width: 34px;
        height: 34px;
        border-radius: 9px;
        display: grid;
        place-items: center;
        background: var(--plum);
        color: white;
        font-size: 1rem;
    }}

    .brand-name {{
        font-size: 1.05rem;
        font-weight: 750;
        color: var(--plum);
    }}

    .page-title {{
        font-size: clamp(1.8rem, 5vw, 2.4rem);
        font-weight: 780;
        letter-spacing: -.035em;
        color: var(--plum);
        margin: 0 0 .15rem;
    }}

    .page-subtitle {{
        color: var(--muted);
        font-size: .93rem;
        margin-bottom: 1.25rem;
    }}

    .add-wrap {{
        background: white;
        border: 1px solid var(--border);
        border-radius: 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,.025);
        padding: .2rem .6rem .05rem;
        margin-bottom: 1rem;
    }}

    div[data-testid="stForm"] {{
        border: 0;
        background: transparent;
        padding: 0;
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="select"] > div {{
        border-radius: 8px !important;
        border-color: #DDDADF !important;
        box-shadow: none !important;
        background: white !important;
    }}

    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {{
        border-color: var(--mauve) !important;
    }}

    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {{
        border-radius: 8px;
        min-height: 39px;
        font-weight: 650;
        border: 1px solid #D8D5DA;
        box-shadow: none;
    }}

    div[data-testid="stFormSubmitButton"] button[kind="primary"] {{
        background: var(--plum);
        border-color: var(--plum);
        color: white;
    }}

    .list-label {{
        color: var(--muted);
        font-size: .78rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin: 1.25rem 0 .5rem;
    }}

    .item-name {{
        font-size: .98rem;
        font-weight: 600;
        color: var(--text);
        line-height: 1.25;
        padding-top: .1rem;
    }}

    .item-name.done {{
        color: #969198;
        text-decoration: line-through;
        font-weight: 500;
    }}

    .item-meta {{
        color: var(--muted);
        font-size: .79rem;
        margin-top: .18rem;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white;
        border: 1px solid var(--border) !important;
        border-radius: 9px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,.02);
    }}

    div[data-testid="stCheckbox"] {{
        padding-top: .15rem;
    }}

    div[data-testid="stCheckbox"] label span[data-baseweb="checkbox"] > div {{
        border-radius: 50%;
    }}

    .count-line {{
        display: flex;
        gap: .45rem;
        align-items: center;
        color: var(--muted);
        font-size: .82rem;
        margin-top: .15rem;
    }}

    .dot {{
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--sage);
        display: inline-block;
    }}

    .empty {{
        background: white;
        border: 1px dashed #D8D5DA;
        border-radius: 10px;
        color: var(--muted);
        text-align: center;
        padding: 2.4rem 1rem;
        margin-top: .5rem;
        font-size: .92rem;
    }}

    .sidebar-count {{
        color: var(--muted);
        font-size: .78rem;
        margin-top: -.65rem;
        margin-bottom: .9rem;
    }}

    @media (max-width: 700px) {{
        .block-container {{
            padding: 1rem .8rem 4rem;
        }}

        .page-title {{
            font-size: 1.8rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL DEFAULT 'Geral',
                quantidade REAL NOT NULL DEFAULT 1,
                unidade TEXT NOT NULL DEFAULT 'un',
                prioridade TEXT NOT NULL DEFAULT 'Normal',
                preco_estimado REAL NOT NULL DEFAULT 0,
                preco_pago REAL NOT NULL DEFAULT 0,
                comprado INTEGER NOT NULL DEFAULT 0,
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
            """
        )


def load_items():
    with db() as conn:
        rows = conn.execute(
            """
            SELECT * FROM itens
            ORDER BY comprado ASC, atualizado_em DESC, id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def add_item(nome, categoria, quantidade, unidade):
    now = datetime.now().isoformat(timespec="seconds")
    with db() as conn:
        conn.execute(
            """
            INSERT INTO itens
            (nome, categoria, quantidade, unidade, prioridade,
             preco_estimado, preco_pago, comprado, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, 'Normal', 0, 0, 0, ?, ?)
            """,
            (nome.strip(), categoria, float(quantidade), unidade, now, now),
        )


def toggle_item(item_id, bought):
    with db() as conn:
        conn.execute(
            "UPDATE itens SET comprado = ?, atualizado_em = ? WHERE id = ?",
            (int(bool(bought)), datetime.now().isoformat(timespec="seconds"), item_id),
        )


def delete_item(item_id):
    with db() as conn:
        conn.execute("DELETE FROM itens WHERE id = ?", (item_id,))


def clear_completed():
    with db() as conn:
        conn.execute("DELETE FROM itens WHERE comprado = 1")


def qty_text(value):
    value = float(value)
    return str(int(value)) if value.is_integer() else str(value).replace(".", ",")


init_db()
items = load_items()

pending = [i for i in items if not i["comprado"]]
completed = [i for i in items if i["comprado"]]


with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✓</div>
            <div class="brand-name">Mercado</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    view = st.radio(
        "Visualização",
        ["Minha lista", "Pendentes", "Concluídos"],
        label_visibility="collapsed",
    )

    st.markdown(
        f'<div class="sidebar-count">{len(pending)} pendentes · {len(completed)} concluídos</div>',
        unsafe_allow_html=True,
    )

    category_filter = st.selectbox(
        "Categoria",
        ["Todas"] + CATEGORIES,
    )

    if completed:
        st.divider()
        if st.button("Limpar concluídos", use_container_width=True):
            clear_completed()
            st.rerun()


st.markdown('<h1 class="page-title">Minha lista</h1>', unsafe_allow_html=True)

if items:
    st.markdown(
        f"""
        <div class="count-line">
            <span>{len(pending)} pendentes</span>
            <span class="dot"></span>
            <span>{len(completed)} concluídos</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="page-subtitle">Adicione o que precisa comprar.</div>',
        unsafe_allow_html=True,
    )

st.write("")

with st.container():
    with st.form("add_item", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        name = c1.text_input(
            "Novo item",
            placeholder="Adicionar um item",
            label_visibility="collapsed",
        )
        submit = c2.form_submit_button(
            "Adicionar",
            type="primary",
            use_container_width=True,
        )

        with st.expander("Detalhes opcionais"):
            d1, d2, d3 = st.columns([2, 1, 1])
            category = d1.selectbox("Categoria", CATEGORIES)
            quantity = d2.number_input("Quantidade", min_value=0.1, value=1.0, step=1.0)
            unit = d3.selectbox("Unidade", UNITS)

        if submit:
            if name.strip():
                add_item(name, category, quantity, unit)
                st.rerun()
            else:
                st.warning("Digite o nome do item.")

search = st.text_input(
    "Pesquisar",
    placeholder="Pesquisar na lista",
    label_visibility="collapsed",
)

visible = items[:]

if view == "Pendentes":
    visible = [i for i in visible if not i["comprado"]]
elif view == "Concluídos":
    visible = [i for i in visible if i["comprado"]]

if category_filter != "Todas":
    visible = [i for i in visible if i["categoria"] == category_filter]

if search.strip():
    term = search.strip().casefold()
    visible = [i for i in visible if term in i["nome"].casefold()]


def render_item(item):
    with st.container(border=True):
        check_col, text_col, delete_col = st.columns([0.42, 5.2, 0.58])

        checked = check_col.checkbox(
            "Concluído",
            value=bool(item["comprado"]),
            key=f"item_{item['id']}",
            label_visibility="collapsed",
        )

        if checked != bool(item["comprado"]):
            toggle_item(item["id"], checked)
            st.rerun()

        css_class = "item-name done" if item["comprado"] else "item-name"
        text_col.markdown(
            f'<div class="{css_class}">{item["nome"]}</div>',
            unsafe_allow_html=True,
        )

        details = []
        if float(item["quantidade"]) != 1 or item["unidade"] != "un":
            details.append(f'{qty_text(item["quantidade"])} {item["unidade"]}')
        if item["categoria"] and item["categoria"] != "Geral":
            details.append(item["categoria"])

        if details:
            text_col.markdown(
                f'<div class="item-meta">{" · ".join(details)}</div>',
                unsafe_allow_html=True,
            )

        if delete_col.button(
            "×",
            key=f"delete_{item['id']}",
            help="Excluir item",
            use_container_width=True,
        ):
            delete_item(item["id"])
            st.rerun()


if not visible:
    st.markdown(
        '<div class="empty">Nenhum item por aqui.</div>',
        unsafe_allow_html=True,
    )
else:
    visible_pending = [i for i in visible if not i["comprado"]]
    visible_completed = [i for i in visible if i["comprado"]]

    if visible_pending:
        st.markdown('<div class="list-label">Pendentes</div>', unsafe_allow_html=True)
        for item in visible_pending:
            render_item(item)

    if visible_completed:
        st.markdown('<div class="list-label">Concluídos</div>', unsafe_allow_html=True)
        for item in visible_completed:
            render_item(item)
