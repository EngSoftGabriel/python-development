"""Lista de Tarefas (To-Do List).

Permite adicionar, listar, concluir, editar e remover tarefas.
Os dados são persistidos em um arquivo JSON.
"""

import json
from datetime import datetime
from pathlib import Path

ARQUIVO_TAREFAS = Path(__file__).parent / "tarefas.json"


def carregar_tarefas() -> list[dict]:
    if not ARQUIVO_TAREFAS.exists():
        return []
    with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas: list[dict]) -> None:
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)


def listar(tarefas: list[dict]) -> None:
    if not tarefas:
        print("Nenhuma tarefa cadastrada.\n")
        return
    print("\n--- TAREFAS ---")
    for i, t in enumerate(tarefas, start=1):
        status = "[x]" if t["concluida"] else "[ ]"
        print(f"{i}. {status} {t['descricao']} (criada em {t['criada_em']})")
    print()


def adicionar(tarefas: list[dict]) -> None:
    descricao = input("Descrição da tarefa: ").strip()
    if not descricao:
        print("Descrição vazia. Cancelado.\n")
        return
    tarefas.append({
        "descricao": descricao,
        "concluida": False,
        "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    })
    salvar_tarefas(tarefas)
    print("Tarefa adicionada.\n")


def concluir(tarefas: list[dict]) -> None:
    listar(tarefas)
    try:
        idx = int(input("Número da tarefa para concluir: ")) - 1
        tarefas[idx]["concluida"] = True
        salvar_tarefas(tarefas)
        print("Tarefa concluída.\n")
    except (ValueError, IndexError):
        print("Índice inválido.\n")


def editar(tarefas: list[dict]) -> None:
    listar(tarefas)
    try:
        idx = int(input("Número da tarefa para editar: ")) - 1
        nova = input("Nova descrição: ").strip()
        if nova:
            tarefas[idx]["descricao"] = nova
            salvar_tarefas(tarefas)
            print("Tarefa editada.\n")
    except (ValueError, IndexError):
        print("Índice inválido.\n")


def remover(tarefas: list[dict]) -> None:
    listar(tarefas)
    try:
        idx = int(input("Número da tarefa para remover: ")) - 1
        removida = tarefas.pop(idx)
        salvar_tarefas(tarefas)
        print(f"Removida: {removida['descricao']}\n")
    except (ValueError, IndexError):
        print("Índice inválido.\n")


def menu() -> None:
    tarefas = carregar_tarefas()
    acoes = {
        "1": ("Listar", lambda: listar(tarefas)),
        "2": ("Adicionar", lambda: adicionar(tarefas)),
        "3": ("Concluir", lambda: concluir(tarefas)),
        "4": ("Editar", lambda: editar(tarefas)),
        "5": ("Remover", lambda: remover(tarefas)),
    }
    while True:
        print("=== LISTA DE TAREFAS ===")
        for k, (nome, _) in acoes.items():
            print(f"{k} - {nome}")
        print("0 - Sair")
        op = input("Escolha: ").strip()
        if op == "0":
            print("Até logo!")
            break
        if op in acoes:
            acoes[op][1]()
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    menu()
