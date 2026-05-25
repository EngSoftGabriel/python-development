"""CRUD completo de produtos com SQLite.

Implementa as quatro operações de banco de dados:
Create, Read, Update e Delete usando o módulo sqlite3.
"""

import sqlite3
from pathlib import Path

ARQUIVO_DB = Path(__file__).parent / "produtos.db"


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(ARQUIVO_DB)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela() -> None:
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL CHECK (preco >= 0),
                estoque INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def criar(nome: str, preco: float, estoque: int) -> int:
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
            (nome, preco, estoque),
        )
        return cur.lastrowid


def listar() -> list[sqlite3.Row]:
    with conectar() as conn:
        return conn.execute(
            "SELECT id, nome, preco, estoque FROM produtos ORDER BY id"
        ).fetchall()


def buscar(produto_id: int) -> sqlite3.Row | None:
    with conectar() as conn:
        return conn.execute(
            "SELECT id, nome, preco, estoque FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()


def atualizar(produto_id: int, nome: str, preco: float, estoque: int) -> bool:
    with conectar() as conn:
        cur = conn.execute(
            "UPDATE produtos SET nome = ?, preco = ?, estoque = ? WHERE id = ?",
            (nome, preco, estoque, produto_id),
        )
        return cur.rowcount > 0


def deletar(produto_id: int) -> bool:
    with conectar() as conn:
        cur = conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        return cur.rowcount > 0


def imprimir(produtos: list[sqlite3.Row]) -> None:
    if not produtos:
        print("Nenhum produto cadastrado.\n")
        return
    print(f"\n{'ID':<4} {'NOME':<25} {'PREÇO':>10} {'ESTOQUE':>10}")
    print("-" * 55)
    for p in produtos:
        print(f"{p['id']:<4} {p['nome']:<25} R${p['preco']:>8.2f} {p['estoque']:>10}")
    print()


def entrada_produto() -> tuple[str, float, int] | None:
    try:
        nome = input("Nome: ").strip()
        if not nome:
            print("Nome obrigatório.\n")
            return None
        preco = float(input("Preço: ").replace(",", "."))
        estoque = int(input("Estoque: "))
        return nome, preco, estoque
    except ValueError:
        print("Valor inválido.\n")
        return None


def menu() -> None:
    criar_tabela()
    while True:
        print("=== CRUD PRODUTOS ===")
        print("1 - Criar")
        print("2 - Listar")
        print("3 - Buscar por ID")
        print("4 - Atualizar")
        print("5 - Deletar")
        print("0 - Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            dados = entrada_produto()
            if dados:
                novo_id = criar(*dados)
                print(f"Produto criado com ID {novo_id}.\n")

        elif op == "2":
            imprimir(listar())

        elif op == "3":
            try:
                produto_id = int(input("ID: "))
                p = buscar(produto_id)
                imprimir([p] if p else [])
            except ValueError:
                print("ID inválido.\n")

        elif op == "4":
            try:
                produto_id = int(input("ID a atualizar: "))
            except ValueError:
                print("ID inválido.\n")
                continue
            if not buscar(produto_id):
                print("Produto não encontrado.\n")
                continue
            dados = entrada_produto()
            if dados and atualizar(produto_id, *dados):
                print("Produto atualizado.\n")

        elif op == "5":
            try:
                produto_id = int(input("ID a deletar: "))
                if deletar(produto_id):
                    print("Produto deletado.\n")
                else:
                    print("Produto não encontrado.\n")
            except ValueError:
                print("ID inválido.\n")

        elif op == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    menu()
