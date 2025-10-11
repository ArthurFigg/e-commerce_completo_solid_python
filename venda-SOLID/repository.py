import os
import sqlite3
from typing import List, Optional
from entidades import Produto

class SQLiteProdutoRepository:
    def __init__(self, db_name: str = None):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = db_name or os.path.join(base_dir, "lojas.db")
        self._criar_tabelas()

    def _con(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabelas(self):
        with self._con() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS produto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL,
                    quantidade INTEGER NOT NULL
                )
            """)
            con.commit()

    def adicionar_produto(self, produto: Produto) -> int:
        with self._con() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO produto (nome, preco, quantidade) VALUES (?, ?, ?)",
                (produto.nome, produto.preco, produto.quantidade),
            )
            con.commit()
            return cur.lastrowid

    def buscar_produto(self, produto_id: int) -> Optional[Produto]:
        with self._con() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT id, nome, preco, quantidade FROM produto WHERE id = ?",
                (produto_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return Produto(id=row[0], nome=row[1], preco=row[2], quantidade=row[3])

    def listar_produtos(self) -> List[Produto]:
        with self._con() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT id, nome, preco, quantidade FROM produto ORDER BY nome COLLATE NOCASE ASC"
            )
            rows = cur.fetchall()
            return [Produto(id=r[0], nome=r[1], preco=r[2], quantidade=r[3]) for r in rows]

    def atualizar_produto(self, produto: Produto) -> bool:
        if produto.id is None:
            return False
        with self._con() as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE produto SET nome = ?, preco = ?, quantidade = ? WHERE id = ?",
                (produto.nome, produto.preco, produto.quantidade, produto.id),
            )
            con.commit()
            return cur.rowcount > 0

    def deletar_produto(self, produto_id: int) -> bool:
        with self._con() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM produto WHERE id = ?", (produto_id,))
            con.commit()
            return cur.rowcount > 0
