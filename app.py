from __future__ import annotations

import json
import time
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

# Evita usar uma chave chamada "items" no st.session_state.
# SessionStateProxy já possui o método .items(), o que pode fazer
# st.session_state.items retornar um método em vez da lista salva.
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

    normalized: list[dict] = []
    for raw in value:
        if not isinstance(raw, dict):
            continue

        name = str(raw.get("name", "")).strip()
        if not name:
            continue

        try:
            quantity = float(raw.get("quantity", 1) or 1)
        except (TypeError, ValueError):
            quantity = 1.0

        normalized.append(
            {
                "id": str(raw.get("id") or uuid4()),
                "name": name,
                "quantity": quantity,
                "unit": str(raw.get("unit", "un") or "un"),
                "category": str(raw.get("category", "Outros") or "Outros"),
                "completed": bool(raw.get("completed", False)),
                "favorite": bool(raw.get("favorite", False)),
                "created_at": str(raw.get("created_at") or now_iso()),
                "updated_at": str(raw.get("updated_at") or now_iso()),
            }
        )

    return normalized


def storage_read() -> list[dict]:
    """Lê a lista persistida no localStorage do navegador."""
    try:
        raw = storage.getItem(STORAGE_KEY)
    except Exception:
        return []
    return normalize_items(raw)


def storage_write(items: list[dict]) -> None:
    """Grava a lista no localStorage do navegador."""
    payload = json.dumps(items, ensure_ascii=False)
    storage.setItem(STORAGE_KEY, payload)
    # Dá tempo ao componente de concluir a escrita no browser antes do rerun.
    time.sleep(0.15)


def persist(items: list[dict], message: str | None = None) -> None:
    storage_write(items)
    if message:
        st.session_state["toast_message"] = message
    st.rerun()


def quantity_text(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else f"{value:g}".replace(".", ",")


def find_item(items: list[dict], item_id: str) -> dict | None:
    return next((item for item in items if item["id"] == item_id), None)


def add_item(items: list[dict], name: str, quantity: float, unit: str, category: str) -> None:
    name = name.strip()
    if not name:
        return

    timestamp = now_iso()
    items.insert(
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


def toggle_completed(items: list[dict], item_id: str) -> None:
    item = find_item(items, item_id)
    if item:
        item["completed"] = not item["completed"]
        item["updated_at"] = now_iso()
        persist(items)


def toggle_favorite(items: list[dict], item_id: str) -> None:
    item = find_item(items, item_id)
    if item:
        item["favorite"] = not item["favorite"]
        item["updated_at"] = now_iso()
        persist(items)


def delete_item(items: list[dict], item_id: str) -> None:
    items[:] = [item for item in items if item["id"] != item_id]
    st.session_state["editing_id"] = None
    persist(items, "Item removido")


def render_edit_form(items: list[dict], item: dict) -> None:
    item_id = item["id"]

    with st.container(border=True):
        st.markdown(
            '<div class="edit-heading">Editar item</div>',
            unsafe_allow_html=True,
        )

        with st.form(f"edit_form_{item_id}", border=False):
            name = st.text_input("Item", value=item["name"], max_chars=80)

            c1, c2, c3 = st.columns([1, 1, 1.45], gap="small")
            quantity = c1.number_input(
                "Quantidade",
                min_value=0.1,
                value=float(item["quantity"]),
                step=1.0,
            )
            unit = c2.selectbox(
                "Unidade",
                UNITS,
                index=UNITS.index(item["unit"]) if item["unit"] in UNITS else 0,
            )
            category = c3.selectbox(
                "Categoria",
                CATEGORIES,
                index=(
                    CATEGORIES.index(item["category"])
                    if item["category"] in CATEGORIES
                    else CATEGORIES.index("Outros")
                ),
            )

            save_col, delete_col = st.columns(2, gap="small")
            save = save_col.form_submit_button(
                "Salvar",
                type="primary",
                use_container_width=True,
            )
            remove = delete_col.form_submit_button(
                "Excluir",
                use_container_width=True,
            )

        if save:
            if not name.strip():
                st.error("Digite o nome do item.")
            else:
                current = find_item(items, item_id)
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
                st.session_state["editing_id"] = None
                persist(items, "Item atualizado")

        if remove:
            delete_item(items, item_id)

        if st.button("Cancelar", key=f"cancel_{item_id}"):
            st.session_state["editing_id"] = None
            st.rerun()


def render_item(items: list[dict], item: dict) -> None:
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
                toggle_completed(items, item_id)

        with text_col:
            title_class = "task-name completed" if completed else "task-name"
            st.markdown(
                f"""
                <div class="task-copy-button">
                    <span class="{title_class}">{escape(item['name'])}</span>
                    <span class="task-meta">{quantity_text(item['quantity'])} {escape(item['unit'])} · {escape(item['category'])}</span>
                </div>
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
                toggle_favorite(items, item_id)

        action_col, _ = st.columns([1.2, 5.8], gap="small")
        with action_col:
            if st.button(
                "•••",
                key=f"more_{item_id}",
                use_container_width=True,
                help="Opções do item",
            ):
                current_editing = st.session_state.get("editing_id")
                st.session_state["editing_id"] = None if current_editing == item_id else item_id
                st.rerun()

    if st.session_state.get("editing_id") == item_id:
        render_edit_form(items, item)


def render_add_box(items: list[dict]) -> None:
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
                quantity = c1.number_input(
                    "Quantidade",
                    min_value=0.1,
                    value=1.0,
                    step=1.0,
                )
                unit = c2.selectbox("Unidade", UNITS)
                category = c3.selectbox(
                    "Categoria",
                    CATEGORIES,
                    index=CATEGORIES.index("Outros"),
                )

            submitted = st.form_submit_button(
                "＋ Adicionar",
                type="primary",
                use_container_width=True,
            )

        if submitted and name.strip():
            add_item(items, name, quantity, unit, category)
            persist(items, "Item adicionado")


if "editing_id" not in st.session_state:
    st.session_state["editing_id"] = None
if "toast_message" not in st.session_state:
    st.session_state["toast_message"] = None

if st.session_state["toast_message"]:
    st.toast(st.session_state["toast_message"])
    st.session_state["toast_message"] = None

# Importante: usamos uma variável Python normal para a lista. Assim evitamos
# colisão com st.session_state.items(), que é um método interno do Streamlit.
items = storage_read()

pending = sorted(
    [item for item in items if not item["completed"]],
    key=lambda item: (not item["favorite"], item["created_at"]),
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

search = st.text_input(
    "Buscar",
    placeholder="Buscar item",
    label_visibility="collapsed",
).strip().casefold()

if search:
    pending = [item for item in pending if search in item["name"].casefold()]
    completed = [item for item in completed if search in item["name"].casefold()]

if pending:
    for item in pending:
        render_item(items, item)
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

with st.expander(
    f"✓ Concluída ({len(completed)})",
    expanded=bool(completed),
):
    for item in completed:
        render_item(items, item)

    if completed and st.button("Limpar concluídos", use_container_width=True):
        items[:] = [item for item in items if not item["completed"]]
        persist(items, "Concluídos removidos")

st.markdown('<div class="add-spacer"></div>', unsafe_allow_html=True)
render_add_box(items)
st.markdown('<div class="bottom-safe-area"></div>', unsafe_allow_html=True)
