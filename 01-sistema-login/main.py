"""Sistema de Login com cadastro, validação e hash de senhas.

Conceitos aplicados: manipulação de dados, validação de formulários,
hash de senhas (SHA-256) e persistência em arquivo JSON.
"""

import hashlib
import json
import re
from pathlib import Path

ARQUIVO_USUARIOS = Path(__file__).parent / "usuarios.json"


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def carregar_usuarios() -> dict:
    if not ARQUIVO_USUARIOS.exists():
        return {}
    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_usuarios(usuarios: dict) -> None:
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)


def email_valido(email: str) -> bool:
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None


def senha_valida(senha: str) -> tuple[bool, str]:
    if len(senha) < 8:
        return False, "A senha precisa ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return False, "A senha precisa ter pelo menos uma letra maiúscula."
    if not re.search(r"\d", senha):
        return False, "A senha precisa ter pelo menos um número."
    return True, "OK"


def cadastrar() -> None:
    usuarios = carregar_usuarios()
    email = input("E-mail: ").strip().lower()

    if not email_valido(email):
        print("E-mail inválido.\n")
        return
    if email in usuarios:
        print("E-mail já cadastrado.\n")
        return

    senha = input("Senha: ")
    ok, msg = senha_valida(senha)
    if not ok:
        print(f"{msg}\n")
        return

    usuarios[email] = {"senha_hash": hash_senha(senha)}
    salvar_usuarios(usuarios)
    print("Cadastro realizado com sucesso!\n")


def login() -> None:
    usuarios = carregar_usuarios()
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ")

    usuario = usuarios.get(email)
    if usuario and usuario["senha_hash"] == hash_senha(senha):
        print(f"Bem-vindo(a), {email}!\n")
    else:
        print("E-mail ou senha incorretos.\n")


def menu() -> None:
    while True:
        print("=== SISTEMA DE LOGIN ===")
        print("1 - Cadastrar")
        print("2 - Entrar")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            login()
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    menu()
