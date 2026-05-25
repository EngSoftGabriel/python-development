"""Bot de automação: baixa arquivos a partir de uma lista de URLs.

Exemplo de bot que automatiza uma tarefa repetitiva: dado um arquivo
de texto com URLs (uma por linha), baixa cada arquivo para a pasta
'downloads/' mostrando o progresso.
"""

import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

PASTA = Path(__file__).parent
PASTA_DOWNLOADS = PASTA / "downloads"
ARQUIVO_URLS = PASTA / "urls.txt"
TIMEOUT = 30


def nome_do_arquivo(url: str, indice: int) -> str:
    caminho = urlparse(url).path
    nome = Path(caminho).name
    if not nome:
        nome = f"arquivo_{indice}.bin"
    return nome


def baixar(url: str, destino: Path) -> bool:
    try:
        with requests.get(url, stream=True, timeout=TIMEOUT) as resp:
            resp.raise_for_status()
            total = int(resp.headers.get("content-length", 0))
            baixado = 0
            with open(destino, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    f.write(chunk)
                    baixado += len(chunk)
                    if total:
                        pct = baixado * 100 // total
                        print(f"\r  {destino.name}: {pct}%", end="", flush=True)
        print(f"\r  {destino.name}: OK ({baixado / 1024:.1f} KB)")
        return True
    except requests.RequestException as e:
        print(f"\r  {destino.name}: erro -> {e}")
        return False


def carregar_urls() -> list[str]:
    if not ARQUIVO_URLS.exists():
        exemplos = [
            "https://www.python.org/static/img/python-logo.png",
            "https://raw.githubusercontent.com/python/cpython/main/README.rst",
        ]
        ARQUIVO_URLS.write_text("\n".join(exemplos), encoding="utf-8")
        print(f"Arquivo {ARQUIVO_URLS.name} criado com URLs de exemplo.\n")
    return [
        linha.strip()
        for linha in ARQUIVO_URLS.read_text(encoding="utf-8").splitlines()
        if linha.strip() and not linha.startswith("#")
    ]


def executar() -> None:
    PASTA_DOWNLOADS.mkdir(exist_ok=True)
    urls = carregar_urls()
    if not urls:
        print("Nenhuma URL para baixar.")
        return

    print(f"Iniciando download de {len(urls)} arquivo(s)...\n")
    sucesso = 0
    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] {url}")
        destino = PASTA_DOWNLOADS / nome_do_arquivo(url, i)
        if baixar(url, destino):
            sucesso += 1
    print(f"\nConcluído: {sucesso}/{len(urls)} baixado(s) com sucesso.")
    print(f"Pasta: {PASTA_DOWNLOADS}")


if __name__ == "__main__":
    try:
        executar()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        sys.exit(0)
