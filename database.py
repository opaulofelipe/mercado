from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

DB_PATH = Path(__file__).with_name("mercado.db")


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL DEFAULT 'Outros',
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
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_itens_comprado ON itens(comprado)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_itens_categoria ON itens(categoria)"
        )


def list_items() -> list[dict]:
    with connection() as conn:
        rows = conn.execute(
            """
            SELECT id, nome, categoria, quantidade, unidade, comprado,
                   criado_em, atualizado_em
            FROM itens
            ORDER BY comprado ASC, id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def add_item(
    nome: str,
    categoria: str = "Outros",
    quantidade: float = 1,
    unidade: str = "un",
) -> None:
    nome = nome.strip()
    if not nome:
        raise ValueError("O nome do item não pode ficar vazio.")

    now = datetime.now().isoformat(timespec="seconds")
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO itens (
                nome, categoria, quantidade, unidade, prioridade,
                preco_estimado, preco_pago, comprado, criado_em, atualizado_em
            )
            VALUES (?, ?, ?, ?, 'Normal', 0, 0, 0, ?, ?)
            """,
            (nome, categoria, float(quantidade), unidade, now, now),
        )


def set_completed(item_id: int, completed: bool) -> None:
    with connection() as conn:
        conn.execute(
            """
            UPDATE itens
            SET comprado = ?, atualizado_em = ?
            WHERE id = ?
            """,
            (
                int(bool(completed)),
                datetime.now().isoformat(timespec="seconds"),
                item_id,
            ),
        )


def update_item(
    item_id: int,
    nome: str,
    categoria: str,
    quantidade: float,
    unidade: str,
) -> None:
    nome = nome.strip()
    if not nome:
        raise ValueError("O nome do item não pode ficar vazio.")

    with connection() as conn:
        conn.execute(
            """
            UPDATE itens
            SET nome = ?, categoria = ?, quantidade = ?, unidade = ?,
                atualizado_em = ?
            WHERE id = ?
            """,
            (
                nome,
                categoria,
                float(quantidade),
                unidade,
                datetime.now().isoformat(timespec="seconds"),
                item_id,
            ),
        )


def delete_item(item_id: int) -> None:
    with connection() as conn:
        conn.execute("DELETE FROM itens WHERE id = ?", (item_id,))


def delete_completed() -> int:
    with connection() as conn:
        cursor = conn.execute("DELETE FROM itens WHERE comprado = 1")
        return cursor.rowcount
