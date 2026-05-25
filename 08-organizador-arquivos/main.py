"""Organizador automático de arquivos por categoria.

Move os arquivos da pasta indicada para subpastas baseadas na
extensão (Imagens, Documentos, Vídeos, Áudios, Compactados, Códigos,
Outros). Use --dry-run para simular antes de mover.
"""

import argparse
import shutil
from pathlib import Path

CATEGORIAS: dict[str, set[str]] = {
    "Imagens":     {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documentos":  {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf",
                    ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Videos":      {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"},
    "Audios":      {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Codigos":     {".py", ".js", ".ts", ".html", ".css", ".java", ".c",
                    ".cpp", ".cs", ".go", ".rs", ".rb", ".php", ".json", ".xml"},
    "Executaveis": {".exe", ".msi", ".bat", ".sh", ".apk"},
}


def categoria_para(extensao: str) -> str:
    ext = extensao.lower()
    for nome, exts in CATEGORIAS.items():
        if ext in exts:
            return nome
    return "Outros"


def organizar(pasta: Path, dry_run: bool = False) -> None:
    if not pasta.is_dir():
        print(f"Pasta não encontrada: {pasta}")
        return

    arquivos = [item for item in pasta.iterdir() if item.is_file()]
    if not arquivos:
        print("Nenhum arquivo para organizar.")
        return

    movidos: dict[str, int] = {}
    for arquivo in arquivos:
        if arquivo.name == Path(__file__).name:
            continue
        categoria = categoria_para(arquivo.suffix)
        destino_dir = pasta / categoria
        destino = destino_dir / arquivo.name

        acao = "Moveria" if dry_run else "Movendo"
        print(f"{acao}: {arquivo.name} -> {categoria}/")

        if not dry_run:
            destino_dir.mkdir(exist_ok=True)
            if destino.exists():
                base, suf = arquivo.stem, arquivo.suffix
                i = 1
                while (destino_dir / f"{base}_{i}{suf}").exists():
                    i += 1
                destino = destino_dir / f"{base}_{i}{suf}"
            shutil.move(str(arquivo), str(destino))

        movidos[categoria] = movidos.get(categoria, 0) + 1

    print("\n--- RESUMO ---")
    for categoria, qtd in sorted(movidos.items()):
        print(f"{categoria:<15} {qtd}")
    print(f"Total: {sum(movidos.values())} arquivo(s)")
    if dry_run:
        print("(modo dry-run — nada foi movido)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Organizador de arquivos por categoria.")
    parser.add_argument(
        "pasta",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Pasta a organizar (padrão: ~/Downloads)",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Apenas simula sem mover arquivos.")
    args = parser.parse_args()

    pasta = Path(args.pasta).expanduser().resolve()
    print(f"Organizando: {pasta}\n")
    organizar(pasta, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
