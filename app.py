import csv
import io
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="Lista de Mercado",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_PATH = Path(__file__).with_name("mercado.db")

PALETTE = {
    "green": "#9EE493",
    "mint": "#DAF7DC",
    "sage": "#ABC8C0",
    "mauve": "#70566D",
    "plum": "#42273B",
    "white": "#FFFFFF",
    "bg": "#F7FBF8",
    "text": "#2B2530",
    "muted": "#6E6670",
    "danger": "#9B3D54",
}

CATEGORIES = {
    "Hortifruti": "🥬",
    "Padaria": "🥖",
    "Açougue": "🥩",
    "Frios e laticínios": "🧀",
    "Mercearia": "🥫",
    "Bebidas": "🥤",
    "Congelados": "❄️",
    "Higiene": "🧴",
    "Limpeza": "🧽",
    "Pet": "🐾",
    "Outros": "🛍️",
}

UNITS = ["un", "kg", "g", "L", "mL", "pct", "cx", "dz"]
PRIORITIES = ["Normal", "Importante", "Essencial"]


# =========================================================
# ESTILO
# =========================================================
st.markdown(
    f"""
    <style>
        :root {{
            --green: {PALETTE["green"]};
            --mint: {PALETTE["mint"]};
            --sage: {PALETTE["sage"]};
            --mauve: {PALETTE["mauve"]};
            --plum: {PALETTE["plum"]};
            --bg: {PALETTE["bg"]};
            --text: {PALETTE["text"]};
            --muted: {PALETTE["muted"]};
        }}

        .stApp {{
            background:
                radial-gradient(circle at 5% 0%, rgba(158, 228, 147, .25), transparent 26rem),
                linear-gradient(180deg, #FBFDFC 0%, var(--bg) 100%);
            color: var(--text);
        }}

        .block-container {{
            max-width: 1180px;
            padding-top: 1.8rem;
            padding-bottom: 4rem;
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        #MainMenu, footer {{
            visibility: hidden;
        }}

        .hero {{
            background: linear-gradient(135deg, var(--plum) 0%, var(--mauve) 100%);
            border-radius: 28px;
            padding: 28px 30px;
            margin-bottom: 18px;
            box-shadow: 0 16px 50px rgba(66, 39, 59, .17);
            overflow: hidden;
            position: relative;
        }}

        .hero:after {{
            content: "";
            width: 190px;
            height: 190px;
            border-radius: 999px;
            background: rgba(158, 228, 147, .16);
            position: absolute;
            right: -50px;
            top: -65px;
        }}

        .hero-kicker {{
            color: var(--green);
            text-transform: uppercase;
            letter-spacing: .12em;
            font-weight: 800;
            font-size: .78rem;
            margin-bottom: 8px;
        }}

        .hero-title {{
            color: white;
            font-size: clamp(2rem, 5vw, 3.3rem);
            line-height: 1;
            margin: 0;
            font-weight: 850;
            letter-spacing: -0.04em;
        }}

        .hero-sub {{
            color: rgba(255,255,255,.78);
            font-size: 1rem;
            margin-top: 12px;
            max-width: 650px;
        }}

        .stat-card {{
            background: rgba(255,255,255,.88);
            border: 1px solid rgba(171, 200, 192, .45);
            border-radius: 20px;
            padding: 17px 18px;
            min-height: 108px;
            box-shadow: 0 8px 24px rgba(66,39,59,.06);
        }}

        .stat-label {{
            color: var(--muted);
            font-size: .82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .05em;
        }}

        .stat-value {{
            color: var(--plum);
            font-size: 1.65rem;
            font-weight: 850;
            margin-top: 4px;
            letter-spacing: -0.03em;
        }}

        .stat-hint {{
            color: var(--muted);
            font-size: .79rem;
            margin-top: 3px;
        }}

        .section-title {{
            color: var(--plum);
            font-size: 1.25rem;
            font-weight: 850;
            margin: 1.15rem 0 .15rem;
            letter-spacing: -.02em;
        }}

        .section-sub {{
            color: var(--muted);
            font-size: .88rem;
            margin-bottom: .8rem;
        }}

        .category-title {{
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            background: var(--mint);
            color: var(--plum);
            padding: .48rem .8rem;
            border-radius: 999px;
            font-weight: 800;
            font-size: .9rem;
            margin: .8rem 0 .45rem;
        }}

        div[data-testid="stForm"] {{
            border: 1px solid rgba(171, 200, 192, .55);
            border-radius: 22px;
            background: rgba(255,255,255,.80);
            padding: 8px 12px 3px;
            box-shadow: 0 8px 28px rgba(66,39,59,.05);
        }}

        div[data-testid="stMetric"] {{
            background: white;
            border: 1px solid rgba(171, 200, 192, .45);
            padding: 12px 14px;
            border-radius: 18px;
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-baseweb="select"] > div {{
            border-radius: 14px !important;
        }}

        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button {{
            border-radius: 14px;
            font-weight: 750;
            min-height: 42px;
            transition: transform .15s ease, box-shadow .15s ease;
        }}

        div[data-testid="stButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 7px 18px rgba(66, 39, 59, .10);
        }}

        .item-line {{
            color: var(--muted);
            font-size: .84rem;
            margin-top: -4px;
        }}

        .bought-note {{
            color: var(--muted);
            font-size: .85rem;
        }}

        .empty {{
            border: 1px dashed rgba(112, 86, 109, .30);
            border-radius: 22px;
            padding: 35px 22px;
            text-align: center;
            color: var(--muted);
            background: rgba(218,247,220,.26);
            margin-top: .8rem;
        }}

        .empty strong {{
            color: var(--plum);
            font-size: 1.05rem;
        }}

        div[data-testid="stProgress"] > div > div > div > div {{
            background-color: var(--green);
        }}

        @media (max-width: 700px) {{
            .block-container {{
                padding-left: .85rem;
                padding-right: .85rem;
                padding-top: .9rem;
            }}

            .hero {{
                border-radius: 22px;
                padding: 23px 20px;
            }}

            .stat-card {{
                min-height: 96px;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# BANCO DE DADOS
# =========================================================
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
                categoria TEXT NOT NULL,
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


def add_item(nome, categoria, quantidade, unidade, prioridade, preco_estimado):
    now = datetime.now().isoformat(timespec="seconds")
    with db() as conn:
        conn.execute(
            """
            INSERT INTO itens
                (nome, categoria, quantidade, unidade, prioridade,
                 preco_estimado, preco_pago, comprado, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?, ?)
            """,
            (
                nome.strip(),
                categoria,
                float(quantidade),
                unidade,
                prioridade,
                float(preco_estimado or 0),
                now,
                now,
            ),
        )


def update_item(
    item_id,
    nome,
    categoria,
    quantidade,
    unidade,
    prioridade,
    preco_estimado,
    preco_pago,
):
    with db() as conn:
        conn.execute(
            """
            UPDATE itens
            SET nome = ?, categoria = ?, quantidade = ?, unidade = ?,
                prioridade = ?, preco_estimado = ?, preco_pago = ?, atualizado_em = ?
            WHERE id = ?
            """,
            (
                nome.strip(),
                categoria,
                float(quantidade),
                unidade,
                prioridade,
                float(preco_estimado or 0),
                float(preco_pago or 0),
                datetime.now().isoformat(timespec="seconds"),
                item_id,
            ),
        )


def toggle_item(item_id, bought):
    with db() as conn:
        conn.execute(
            """
            UPDATE itens
            SET comprado = ?, atualizado_em = ?
            WHERE id = ?
            """,
            (
                int(bool(bought)),
                datetime.now().isoformat(timespec="seconds"),
                item_id,
            ),
        )


def delete_item(item_id):
    with db() as conn:
        conn.execute("DELETE FROM itens WHERE id = ?", (item_id,))


def mark_all(bought=True):
    with db() as conn:
        conn.execute(
            "UPDATE itens SET comprado = ?, atualizado_em = ?",
            (
                int(bool(bought)),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )


def clear_bought():
    with db() as conn:
        conn.execute("DELETE FROM itens WHERE comprado = 1")


def load_items():
    with db() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM itens
            ORDER BY
                comprado ASC,
                CASE prioridade
                    WHEN 'Essencial' THEN 1
                    WHEN 'Importante' THEN 2
                    ELSE 3
                END,
                categoria ASC,
                nome COLLATE NOCASE ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


# =========================================================
# HELPERS
# =========================================================
def brl(value):
    value = float(value or 0)
    return "R$ " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def qty_text(value):
    value = float(value)
    return str(int(value)) if value.is_integer() else str(value).replace(".", ",")


def priority_icon(priority):
    return {
        "Normal": "•",
        "Importante": "◆",
        "Essencial": "★",
    }.get(priority, "•")


def dataframe_csv(items):
    if not items:
        return b""
    df = pd.DataFrame(items)
    rename = {
        "nome": "Item",
        "categoria": "Categoria",
        "quantidade": "Quantidade",
        "unidade": "Unidade",
        "prioridade": "Prioridade",
        "preco_estimado": "Preço estimado",
        "preco_pago": "Preço pago",
        "comprado": "Comprado",
        "criado_em": "Criado em",
        "atualizado_em": "Atualizado em",
    }
    df = df.rename(columns=rename)
    if "Comprado" in df:
        df["Comprado"] = df["Comprado"].map({0: "Não", 1: "Sim"})
    return df.to_csv(index=False).encode("utf-8-sig")


def set_editing(item_id):
    st.session_state["editing_id"] = item_id


# =========================================================
# INICIALIZAÇÃO
# =========================================================
init_db()
items = load_items()

if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

# =========================================================
# CABEÇALHO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Sua compra, sem bagunça</div>
        <h1 class="hero-title">Lista de mercado.</h1>
        <div class="hero-sub">
            Organize por categoria, acompanhe o orçamento e marque os itens
            conforme coloca tudo no carrinho.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

total = len(items)
bought_count = sum(int(i["comprado"]) for i in items)
pending_count = total - bought_count
progress = bought_count / total if total else 0.0
estimated_total = sum(float(i["preco_estimado"] or 0) for i in items)
paid_total = sum(float(i["preco_pago"] or 0) for i in items if i["comprado"])

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Pendentes</div>
            <div class="stat-value">{pending_count}</div>
            <div class="stat-hint">item(ns) ainda na lista</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Progresso</div>
            <div class="stat-value">{round(progress * 100)}%</div>
            <div class="stat-hint">{bought_count} de {total} concluído(s)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Estimativa</div>
            <div class="stat-value">{brl(estimated_total)}</div>
            <div class="stat-hint">planejado para a compra</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s4:
    difference = paid_total - estimated_total if paid_total else 0
    hint = (
        f"{brl(abs(difference))} {'acima' if difference > 0 else 'abaixo'} da estimativa"
        if paid_total and difference != 0
        else "valor efetivamente registrado"
    )
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Pago</div>
            <div class="stat-value">{brl(paid_total)}</div>
            <div class="stat-hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.progress(progress)

# =========================================================
# ADICIONAR ITEM
# =========================================================
st.markdown('<div class="section-title">Adicionar item</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Cadastre só o necessário. Preço é opcional e pode ser ajustado depois.</div>',
    unsafe_allow_html=True,
)

with st.form("add_item_form", clear_on_submit=True):
    r1 = st.columns([2.3, 1.35, .75, .8])
    nome = r1[0].text_input(
        "Produto",
        placeholder="Ex.: Café, banana, detergente…",
        max_chars=80,
    )
    categoria = r1[1].selectbox("Categoria", list(CATEGORIES.keys()))
    quantidade = r1[2].number_input(
        "Qtd.",
        min_value=0.1,
        value=1.0,
        step=1.0,
    )
    unidade = r1[3].selectbox("Unidade", UNITS)

    r2 = st.columns([1.25, 1.1, 2.05])
    prioridade = r2[0].selectbox("Prioridade", PRIORITIES)
    preco_estimado = r2[1].number_input(
        "Preço estimado (R$)",
        min_value=0.0,
        value=0.0,
        step=0.50,
        format="%.2f",
    )
    submitted = r2[2].form_submit_button(
        "＋ Adicionar à lista",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        if not nome.strip():
            st.error("Digite o nome do produto.")
        else:
            add_item(
                nome,
                categoria,
                quantidade,
                unidade,
                prioridade,
                preco_estimado,
            )
            st.rerun()

# =========================================================
# FILTROS E AÇÕES
# =========================================================
st.markdown('<div class="section-title">Sua lista</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns([1.7, 1.15, 1.5])
search = f1.text_input(
    "Buscar",
    placeholder="Filtrar por nome…",
    label_visibility="collapsed",
)
status = f2.selectbox(
    "Status",
    ["Pendentes", "Todos", "Comprados"],
    label_visibility="collapsed",
)
category_filter = f3.multiselect(
    "Categorias",
    list(CATEGORIES.keys()),
    placeholder="Todas as categorias",
    label_visibility="collapsed",
)

action1, action2, action3, action4 = st.columns([1.1, 1.1, 1.1, 1.25])
if action1.button(
    "✓ Marcar tudo",
    use_container_width=True,
    disabled=not items or pending_count == 0,
):
    mark_all(True)
    st.rerun()

if action2.button(
    "↺ Desmarcar tudo",
    use_container_width=True,
    disabled=not items or bought_count == 0,
):
    mark_all(False)
    st.rerun()

if action3.button(
    "🗑 Limpar comprados",
    use_container_width=True,
    disabled=bought_count == 0,
):
    clear_bought()
    st.rerun()

action4.download_button(
    "⇩ Exportar CSV",
    data=dataframe_csv(items),
    file_name=f"lista_mercado_{datetime.now():%Y-%m-%d}.csv",
    mime="text/csv",
    use_container_width=True,
    disabled=not items,
)

filtered = items[:]

if search.strip():
    needle = search.strip().casefold()
    filtered = [i for i in filtered if needle in i["nome"].casefold()]

if status == "Pendentes":
    filtered = [i for i in filtered if not i["comprado"]]
elif status == "Comprados":
    filtered = [i for i in filtered if i["comprado"]]

if category_filter:
    filtered = [i for i in filtered if i["categoria"] in category_filter]

# =========================================================
# EDITOR
# =========================================================
editing = None
if st.session_state.editing_id is not None:
    editing = next(
        (i for i in items if i["id"] == st.session_state.editing_id),
        None,
    )

if editing:
    with st.expander(
        f"✎ Editando: {editing['nome']}",
        expanded=True,
    ):
        with st.form(f"edit_form_{editing['id']}"):
            e1 = st.columns([2.2, 1.35, .75, .8])
            e_nome = e1[0].text_input("Produto", value=editing["nome"])
            e_categoria = e1[1].selectbox(
                "Categoria",
                list(CATEGORIES.keys()),
                index=list(CATEGORIES.keys()).index(editing["categoria"])
                if editing["categoria"] in CATEGORIES
                else len(CATEGORIES) - 1,
            )
            e_quantidade = e1[2].number_input(
                "Qtd.",
                min_value=0.1,
                value=float(editing["quantidade"]),
                step=1.0,
            )
            e_unidade = e1[3].selectbox(
                "Unidade",
                UNITS,
                index=UNITS.index(editing["unidade"])
                if editing["unidade"] in UNITS
                else 0,
            )

            e2 = st.columns([1.2, 1.1, 1.1, 1.4])
            e_prioridade = e2[0].selectbox(
                "Prioridade",
                PRIORITIES,
                index=PRIORITIES.index(editing["prioridade"])
                if editing["prioridade"] in PRIORITIES
                else 0,
            )
            e_estimado = e2[1].number_input(
                "Estimado (R$)",
                min_value=0.0,
                value=float(editing["preco_estimado"] or 0),
                step=0.50,
                format="%.2f",
            )
            e_pago = e2[2].number_input(
                "Pago (R$)",
                min_value=0.0,
                value=float(editing["preco_pago"] or 0),
                step=0.50,
                format="%.2f",
            )
            save = e2[3].form_submit_button(
                "Salvar alterações",
                type="primary",
                use_container_width=True,
            )

            if save:
                if not e_nome.strip():
                    st.error("Digite o nome do produto.")
                else:
                    update_item(
                        editing["id"],
                        e_nome,
                        e_categoria,
                        e_quantidade,
                        e_unidade,
                        e_prioridade,
                        e_estimado,
                        e_pago,
                    )
                    st.session_state.editing_id = None
                    st.rerun()

        if st.button("Cancelar edição", key=f"cancel_{editing['id']}"):
            st.session_state.editing_id = None
            st.rerun()

# =========================================================
# LISTA
# =========================================================
if not filtered:
    st.markdown(
        """
        <div class="empty">
            <strong>Nenhum item encontrado.</strong><br>
            Adicione um produto ou ajuste os filtros.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    category_order = list(CATEGORIES.keys())

    for category in category_order:
        cat_items = [i for i in filtered if i["categoria"] == category]
        if not cat_items:
            continue

        st.markdown(
            f'<div class="category-title">{CATEGORIES.get(category, "🛍️")} {category} · {len(cat_items)}</div>',
            unsafe_allow_html=True,
        )

        for item in cat_items:
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([.42, 4.0, 1.25, 1.1])

                new_value = c1.checkbox(
                    "Comprado",
                    value=bool(item["comprado"]),
                    key=f"check_{item['id']}",
                    label_visibility="collapsed",
                )

                if new_value != bool(item["comprado"]):
                    toggle_item(item["id"], new_value)
                    st.rerun()

                name_style = (
                    "text-decoration: line-through; opacity: .55;"
                    if item["comprado"]
                    else ""
                )
                c2.markdown(
                    f"""
                    <div style="font-size:1rem;font-weight:820;color:{PALETTE["plum"]};{name_style}">
                        {item["nome"]}
                    </div>
                    <div class="item-line">
                        {qty_text(item["quantidade"])} {item["unidade"]}
                        &nbsp;·&nbsp; {priority_icon(item["prioridade"])} {item["prioridade"]}
                        &nbsp;·&nbsp; estimado {brl(item["preco_estimado"])}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if item["comprado"] and float(item["preco_pago"] or 0) > 0:
                    c3.markdown(
                        f"**{brl(item['preco_pago'])}**  \n<span class='bought-note'>pago</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    c3.markdown(
                        f"**{brl(item['preco_estimado'])}**  \n<span class='bought-note'>estimado</span>",
                        unsafe_allow_html=True,
                    )

                with c4:
                    a, b = st.columns(2)
                    if a.button(
                        "✎",
                        key=f"edit_{item['id']}",
                        help="Editar item",
                        use_container_width=True,
                    ):
                        set_editing(item["id"])
                        st.rerun()

                    if b.button(
                        "×",
                        key=f"delete_{item['id']}",
                        help="Excluir item",
                        use_container_width=True,
                    ):
                        delete_item(item["id"])
                        if st.session_state.editing_id == item["id"]:
                            st.session_state.editing_id = None
                        st.rerun()

st.caption(
    "Dados salvos localmente em mercado.db. "
    "Ao publicar em hospedagens efêmeras, use um banco persistente se quiser manter a lista entre reinicializações."
)
