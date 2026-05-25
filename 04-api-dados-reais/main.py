"""Consumo de APIs públicas com a biblioteca requests.

Consulta CEP (ViaCEP) e cotação de moedas (AwesomeAPI) e
exibe os dados de forma organizada no terminal.
"""

import sys

import requests

TIMEOUT = 10


def consultar_cep(cep: str) -> None:
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        print("CEP deve conter 8 dígitos.\n")
        return

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        dados = resp.json()
    except requests.RequestException as e:
        print(f"Erro ao consultar CEP: {e}\n")
        return

    if dados.get("erro"):
        print("CEP não encontrado.\n")
        return

    print("\n--- ENDEREÇO ---")
    print(f"CEP:        {dados.get('cep')}")
    print(f"Logradouro: {dados.get('logradouro')}")
    print(f"Bairro:     {dados.get('bairro')}")
    print(f"Cidade:     {dados.get('localidade')} - {dados.get('uf')}")
    print(f"DDD:        {dados.get('ddd')}\n")


def consultar_cotacao(par: str = "USD-BRL") -> None:
    url = f"https://economia.awesomeapi.com.br/json/last/{par}"
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        dados = resp.json()
    except requests.RequestException as e:
        print(f"Erro ao consultar cotação: {e}\n")
        return

    chave = par.replace("-", "")
    info = dados.get(chave)
    if not info:
        print("Par de moedas não encontrado.\n")
        return

    print(f"\n--- COTAÇÃO {info['code']} / {info['codein']} ---")
    print(f"Nome:    {info['name']}")
    print(f"Compra:  R$ {float(info['bid']):.4f}")
    print(f"Venda:   R$ {float(info['ask']):.4f}")
    print(f"Máxima:  R$ {float(info['high']):.4f}")
    print(f"Mínima:  R$ {float(info['low']):.4f}")
    print(f"Variação: {info['varBid']}\n")


def menu() -> None:
    while True:
        print("=== API - DADOS REAIS ===")
        print("1 - Consultar CEP (ViaCEP)")
        print("2 - Cotação USD/BRL")
        print("3 - Cotação EUR/BRL")
        print("4 - Cotação personalizada (ex: BTC-BRL)")
        print("0 - Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            consultar_cep(input("CEP: "))
        elif op == "2":
            consultar_cotacao("USD-BRL")
        elif op == "3":
            consultar_cotacao("EUR-BRL")
        elif op == "4":
            consultar_cotacao(input("Par (ex: BTC-BRL): ").upper())
        elif op == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        sys.exit(0)
