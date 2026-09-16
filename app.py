from __future__ import annotations

import json
from datetime import datetime
from html import escape
from uuid import uuid4

import streamlit as st
from streamlit_local_storage import LocalStorage

from styles import inject_styles


st.set_page_config(
    page_title="Mercado",
    page_icon="✓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles()

STORAGE_KEY = "mercado_items_v1"
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

storage = LocalStorage()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def normalize_items(value) -> list[dict]:
    if value in (None, "", []):
        return []

    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []

    if not isinstance(value, list):
        return []

    normalized = []
    for raw in value:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name", "")).strip()
        if not name:
            continue
        normalized.append(
            {
                "id": str(raw.get("id") or uuid4()),
                "name": name,
                "quantity": float(raw.get("quantity", 1) or 1),
                "unit": str(raw.get("unit", "un") or "un"),
                "category": str(raw.get("category", "Outros") or "Outros"),
                "completed": bool(raw.get("completed", False)),
                "favorite": bool(raw.get("favorite", False)),
                "created_at": str(raw.get("created_at", now_iso())),
                "updated_at": str(raw.get("updated_at", now_iso())),
            }
        )
    return normalized


def storage_write(items: list[dict]) -> None:
    st.session_state.save_revision = st.session_state.get("save_revision", 0) + 1
    storage.setItem(
        STORAGE_KEY,
        json.dumps(items, ensure_ascii=False),
        key=f"mercado_save_{st.session_state.save_revision}",
    )


def persist_and_rerun(message: str | None = None) -> None:
    storage_write(st.session_state.items)
    if message:
        st.session_state.toast_message = message
    st.rerun()


def quantity_text(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else f"{value:g}".replace(".", ",")


def find_item(item_id: str) -> dict | None:
    return next((item for item in st.session_state.items if item["id"] == item_id), None)


def add_item(name: str, quantity: float, unit: str, category: str) -> None:
    name = name.strip()
    if not name:
        return
    timestamp = now_iso()
    st.session_state.items.insert(
        0,
        {
            "id": str(uuid4()),
            "name": name,
            "quantity": float(quantity),
            "unit": unit,
            "category": category,
            "completed": False,
            "favorite": False,
            "created_at": timestamp,
            "updated_at": timestamp,
        },
    )


def toggle_completed(item_id: str) -> None:
    item = find_item(item_id)
    if item:
        item["completed"] = not item["completed"]
        item["updated_at"] = now_iso()
        persist_and_rerun()


def toggle_favorite(item_id: str) -> None:
    item = find_item(item_id)
    if item:
        item["favorite"] = not item["favorite"]
        item["updated_at"] = now_iso()
        persist_and_rerun()


def delete_item(item_id: str) -> None:
    st.session_state.items = [item for item in st.session_state.items if item["id"] != item_id]
    st.session_state.editing_id = None
    persist_and_rerun("Item removido")


def render_item(item: dict) -> None:
    item_id = item["id"]
    completed = item["completed"]

    with st.container(border=True):
        check_col, text_col, star_col = st.columns([0.72, 5.8, 0.72], gap="small")

        with check_col:
            check_label = "✓" if completed else "○"
            if st.button(
                check_label,
                key=f"check_{item_id}",
                help="Marcar como pendente" if completed else "Marcar como concluído",
                use_container_width=True,
            ):
                toggle_completed(item_id)

        with text_col:
            title_class = "task-name completed" if completed else "task-name"
            st.markdown(
                f"""
                <button class="task-copy-button" onclick="return false;" tabindex="-1">
                    <span class="{title_class}">{escape(item['name'])}</span>
                    <span class="task-meta">{quantity_text(item['quantity'])} {escape(item['unit'])} · {escape(item['category'])}</span>
                </button>
                """,
                unsafe_allow_html=True,
            )

        with star_col:
            star = "★" if item["favorite"] else "☆"
            if st.button(
                star,
                key=f"star_{item_id}",
                help="Remover dos favoritos" if item["favorite"] else "Favoritar",
                use_container_width=True,
            ):
                toggle_favorite(item_id)

        action_col, spacer = st.columns([1.2, 5.8], gap="small")
        with action_col:
            if st.button("•••", key=f"more_{item_id}", use_container_width=True, help="Opções do item"):
                st.session_state.editing_id = None if st.session_state.editing_id == item_id else item_id
                st.rerun()

    if st.session_state.editing_id == item_id:
        render_edit_form(item)


def render_edit_form(item: dict) -> None:
    item_id = item["id"]
    with st.container(border=True):
        st.markdown('<div class="edit-heading">Editar item</div>', unsafe_allow_html=True)
        with st.form(f"edit_form_{item_id}", border=False):
            name = st.text_input("Item", value=item["name"], max_chars=80)
            c1, c2, c3 = st.columns([1, 1, 1.45], gap="small")
            quantity = c1.number_input("Quantidade", min_value=0.1, value=float(item["quantity"]), step=1.0)
            unit = c2.selectbox(
                "Unidade",
                UNITS,
                index=UNITS.index(item["unit"]) if item["unit"] in UNITS else 0,
            )
            category = c3.selectbox(
                "Categoria",
                CATEGORIES,
                index=CATEGORIES.index(item["category"]) if item["category"] in CATEGORIES else CATEGORIES.index("Outros"),
            )

            save_col, delete_col = st.columns(2, gap="small")
            save = save_col.form_submit_button("Salvar", type="primary", use_container_width=True)
            remove = delete_col.form_submit_button("Excluir", use_container_width=True)

        if save:
            if not name.strip():
                st.error("Digite o nome do item.")
            else:
                current = find_item(item_id)
                if current:
                    current.update(
                        {
                            "name": name.strip(),
                            "quantity": float(quantity),
                            "unit": unit,
                            "category": category,
                            "updated_at": now_iso(),
                        }
                    )
                st.session_state.editing_id = None
                persist_and_rerun("Item atualizado")

        if remove:
            delete_item(item_id)

        if st.button("Cancelar", key=f"cancel_{item_id}"):
            st.session_state.editing_id = None
            st.rerun()


def render_add_box() -> None:
    with st.container(border=True):
        with st.form("add_form", clear_on_submit=True, border=False):
            name = st.text_input(
                "Novo item",
                placeholder="Adicionar uma tarefa",
                label_visibility="collapsed",
                max_chars=80,
            )

            with st.expander("Quantidade e categoria", expanded=False):
                c1, c2, c3 = st.columns([1, 1, 1.45], gap="small")
                quantity = c1.number_input("Quantidade", min_value=0.1, value=1.0, step=1.0)
                unit = c2.selectbox("Unidade", UNITS)
                category = c3.selectbox("Categoria", CATEGORIES, index=CATEGORIES.index("Outros"))

            submitted = st.form_submit_button("＋ Adicionar", type="primary", use_container_width=True)

        if submitted and name.strip():
            add_item(name, quantity, unit, category)
            persist_and_rerun("Item adicionado")


stored_value = storage.getItem(STORAGE_KEY, key="mercado_load")
if "items" not in st.session_state:
    if "mercado_load" not in st.session_state and stored_value is None:
        st.markdown('<div class="loading-state">Carregando sua lista…</div>', unsafe_allow_html=True)
        st.stop()
    st.session_state.items = normalize_items(st.session_state.get("mercado_load", stored_value))

if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "toast_message" not in st.session_state:
    st.session_state.toast_message = None
if "save_revision" not in st.session_state:
    st.session_state.save_revision = 0

if st.session_state.toast_message:
    st.toast(st.session_state.toast_message)
    st.session_state.toast_message = None

items = st.session_state.items
pending = sorted(
    [item for item in items if not item["completed"]],
    key=lambda item: (not item["favorite"], item["created_at"]),
    reverse=False,
)
completed = [item for item in items if item["completed"]]

st.markdown(
    f"""
    <div class="app-header">
        <div class="app-kicker">Mercado</div>
        <div class="app-title">Minha lista</div>
        <div class="app-meta">{len(pending)} pendente(s) · {len(completed)} concluído(s)</div>
    </div>
    """,
    unsafe_allow_html=True,
)

search = st.text_input("Buscar", placeholder="Buscar item", label_visibility="collapsed").strip().casefold()
if search:
    pending = [item for item in pending if search in item["name"].casefold()]
    completed = [item for item in completed if search in item["name"].casefold()]

if pending:
    for item in pending:
        render_item(item)
else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">Nada pendente</div>
            <div class="empty-copy">Adicione um item ou aproveite a lista zerada.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander(f"✓ Concluída ({len(completed)})", expanded=bool(completed)):
    for item in completed:
        render_item(item)

    if completed:
        if st.button("Limpar concluídos", use_container_width=True):
            st.session_state.items = [item for item in st.session_state.items if not item["completed"]]
            persist_and_rerun("Concluídos removidos")

st.markdown('<div class="add-spacer"></div>', unsafe_allow_html=True)
render_add_box()
st.markdown('<div class="bottom-safe-area"></div>', unsafe_allow_html=True)
