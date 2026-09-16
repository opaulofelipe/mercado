from __future__ import annotations

from html import escape

import streamlit as st

from database import (
    add_item,
    delete_completed,
    delete_item,
    init_db,
    list_items,
    set_completed,
    update_item,
)
from styles import inject_styles


st.set_page_config(
    page_title="Mercado",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
init_db()

CATEGORIES = [
    "Hortifruti",
    "Padaria",
    "Açougue",
    "Frios e laticínios",
    "Mercearia",
    "Bebidas",
    "Congelados",
    "Higiene",
    "Limpeza",
    "Pet",
    "Outros",
]
UNITS = ["un", "kg", "g", "L", "mL", "pct", "cx", "dz"]


def quantity_text(value: float) -> str:
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:g}".replace(".", ",")


def toggle_item(item_id: int, widget_key: str) -> None:
    set_completed(item_id, bool(st.session_state[widget_key]))


def filtered_items(
    items: list[dict],
    view: str,
    search: str,
    category: str,
) -> list[dict]:
    result = items

    if view == "pending":
        result = [item for item in result if not item["comprado"]]
    elif view == "done":
        result = [item for item in result if item["comprado"]]

    if category != "Todas":
        result = [item for item in result if item["categoria"] == category]

    term = search.strip().casefold()
    if term:
        result = [item for item in result if term in item["nome"].casefold()]

    return result


def render_item(item: dict) -> None:
    item_id = int(item["id"])
    checkbox_key = f"item_done_{item_id}"

    with st.container(border=True):
        check_col, text_col, action_col = st.columns([0.55, 6.6, 1.2])

        with check_col:
            st.checkbox(
                f"Marcar {item['nome']} como comprado",
                value=bool(item["comprado"]),
                key=checkbox_key,
                label_visibility="collapsed",
                on_change=toggle_item,
                args=(item_id, checkbox_key),
            )

        with text_col:
            done_class = " done" if item["comprado"] else ""
            st.markdown(
                f'<div class="item-title{done_class}">{escape(item["nome"])}</div>',
                unsafe_allow_html=True,
            )

            metadata = (
                f'{quantity_text(item["quantidade"])} {item["unidade"]}'
                f' · {item["categoria"]}'
            )
            st.markdown(
                f'<div class="item-meta">{metadata}</div>',
                unsafe_allow_html=True,
            )

        with action_col:
            if st.button(
                "Editar",
                key=f"edit_{item_id}",
                use_container_width=True,
                help=f"Editar {item['nome']}",
            ):
                st.session_state.editing_id = (
                    None if st.session_state.get("editing_id") == item_id else item_id
                )
                st.rerun()

    if st.session_state.get("editing_id") == item_id:
        render_edit_form(item)


def render_edit_form(item: dict) -> None:
    item_id = int(item["id"])

    with st.container(border=True):
        st.markdown("**Detalhes do item**")

        with st.form(f"edit_form_{item_id}", border=False):
            name = st.text_input(
                "Item",
                value=item["nome"],
                max_chars=80,
            )

            c1, c2, c3 = st.columns([1, 1, 1.65])
            quantity = c1.number_input(
                "Quantidade",
                min_value=0.1,
                value=float(item["quantidade"]),
                step=1.0,
            )
            unit = c2.selectbox(
                "Unidade",
                UNITS,
                index=UNITS.index(item["unidade"])
                if item["unidade"] in UNITS
                else 0,
            )
            category = c3.selectbox(
                "Categoria",
                CATEGORIES,
                index=CATEGORIES.index(item["categoria"])
                if item["categoria"] in CATEGORIES
                else CATEGORIES.index("Outros"),
            )

            save_col, delete_col = st.columns([1.25, 1])
            save = save_col.form_submit_button(
                "Salvar",
                type="primary",
                use_container_width=True,
            )
            remove = delete_col.form_submit_button(
                "Excluir item",
                use_container_width=True,
            )

        if save:
            try:
                update_item(
                    item_id,
                    name,
                    category,
                    quantity,
                    unit,
                )
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.session_state.editing_id = None
                st.toast("Item atualizado")
                st.rerun()

        if remove:
            delete_item(item_id)
            st.session_state.editing_id = None
            st.toast("Item excluído")
            st.rerun()

        if st.button(
            "Cancelar",
            key=f"cancel_edit_{item_id}",
        ):
            st.session_state.editing_id = None
            st.rerun()


if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

items = list_items()
total = len(items)
done_count = sum(bool(item["comprado"]) for item in items)
pending_count = total - done_count

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">✓</span>Mercado</div>',
        unsafe_allow_html=True,
    )

    view = st.radio(
        "Visualização",
        options=["all", "pending", "done"],
        format_func=lambda value: {
            "all": f"Minha lista  ·  {total}",
            "pending": f"Pendentes  ·  {pending_count}",
            "done": f"Concluídos  ·  {done_count}",
        }[value],
        label_visibility="collapsed",
    )

    st.divider()

    category_filter = st.selectbox(
        "Categoria",
        ["Todas", *CATEGORIES],
    )

    if done_count:
        st.divider()
        if st.button(
            "Limpar concluídos",
            use_container_width=True,
            help="Excluir permanentemente todos os itens concluídos",
        ):
            removed = delete_completed()
            st.session_state.editing_id = None
            st.toast(f"{removed} item(ns) removido(s)")
            st.rerun()

view_title = {
    "all": "Minha lista",
    "pending": "Pendentes",
    "done": "Concluídos",
}[view]

view_meta = {
    "all": f"{pending_count} pendente(s) · {done_count} concluído(s)",
    "pending": f"{pending_count} item(ns) para comprar",
    "done": f"{done_count} item(ns) concluído(s)",
}[view]

st.markdown(f'<h1 class="page-title">{view_title}</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="page-meta">{view_meta}</div>', unsafe_allow_html=True)

st.markdown('<div class="add-caption">Adicionar item</div>', unsafe_allow_html=True)
with st.form("add_item_form", clear_on_submit=True, border=False):
    add_input_col, add_button_col = st.columns([6.6, 1.4])

    with add_input_col:
        new_name = st.text_input(
            "Novo item",
            placeholder="Ex.: café, banana, detergente",
            label_visibility="collapsed",
            max_chars=80,
        )

    with add_button_col:
        submitted = st.form_submit_button(
            "Adicionar",
            type="primary",
            use_container_width=True,
        )

    with st.expander("Quantidade e categoria", expanded=False):
        d1, d2, d3 = st.columns([1, 1, 1.75])
        new_quantity = d1.number_input(
            "Quantidade",
            min_value=0.1,
            value=1.0,
            step=1.0,
        )
        new_unit = d2.selectbox("Unidade", UNITS)
        new_category = d3.selectbox(
            "Categoria",
            CATEGORIES,
            index=CATEGORIES.index("Outros"),
        )

    if submitted:
        try:
            add_item(
                new_name,
                new_category,
                new_quantity,
                new_unit,
            )
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.toast("Item adicionado")
            st.rerun()

search = st.text_input(
    "Buscar na lista",
    placeholder="Buscar",
    label_visibility="collapsed",
)

visible = filtered_items(items, view, search, category_filter)

if not visible:
    st.markdown(
        """
        <div class="empty-state">
            <strong>Nada por aqui</strong>
            Adicione um item ou altere os filtros.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    if view == "all":
        pending = [item for item in visible if not item["comprado"]]
        completed = [item for item in visible if item["comprado"]]

        if pending:
            st.markdown(
                f'<div class="list-label">Pendentes · {len(pending)}</div>',
                unsafe_allow_html=True,
            )
            for item in pending:
                render_item(item)

        if completed:
            with st.expander(
                f"Concluídos ({len(completed)})",
                expanded=False,
            ):
                for item in completed:
                    render_item(item)
    else:
        st.markdown(
            f'<div class="list-label">{len(visible)} item(ns)</div>',
            unsafe_allow_html=True,
        )
        for item in visible:
            render_item(item)
