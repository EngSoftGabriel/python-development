"""Dashboard simples com matplotlib.

Gera um dashboard com 4 gráficos (linha, barras, pizza e dispersão)
a partir de dados de exemplo de vendas mensais por categoria.
"""

import random
from pathlib import Path

import matplotlib.pyplot as plt

PASTA = Path(__file__).parent
ARQUIVO_SAIDA = PASTA / "dashboard.png"

MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
CATEGORIAS = ["Eletrônicos", "Roupas", "Livros", "Alimentos"]


def gerar_dados() -> dict:
    random.seed(42)
    vendas_mensais = [random.randint(8000, 25000) for _ in MESES]
    vendas_categoria = {c: random.randint(15000, 60000) for c in CATEGORIAS}
    investimento = [random.randint(500, 5000) for _ in MESES]
    retorno = [v * random.uniform(1.5, 3.5) for v in investimento]
    return {
        "vendas_mensais": vendas_mensais,
        "vendas_categoria": vendas_categoria,
        "investimento": investimento,
        "retorno": retorno,
    }


def criar_dashboard(dados: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Dashboard de Vendas 2026", fontsize=18, fontweight="bold")

    ax1 = axes[0, 0]
    ax1.plot(MESES, dados["vendas_mensais"], marker="o", color="#2E86DE", linewidth=2)
    ax1.fill_between(MESES, dados["vendas_mensais"], alpha=0.2, color="#2E86DE")
    ax1.set_title("Vendas mensais (R$)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.tick_params(axis="x", rotation=45)

    ax2 = axes[0, 1]
    cats = list(dados["vendas_categoria"].keys())
    valores = list(dados["vendas_categoria"].values())
    barras = ax2.bar(cats, valores, color=["#EE5253", "#10AC84", "#F7B731", "#5F27CD"])
    ax2.set_title("Vendas por categoria")
    ax2.set_ylabel("R$")
    for barra in barras:
        h = barra.get_height()
        ax2.text(barra.get_x() + barra.get_width() / 2, h,
                 f"R$ {h:,.0f}", ha="center", va="bottom", fontsize=9)

    ax3 = axes[1, 0]
    ax3.pie(valores, labels=cats, autopct="%1.1f%%",
            colors=["#EE5253", "#10AC84", "#F7B731", "#5F27CD"],
            startangle=90)
    ax3.set_title("Participação por categoria")

    ax4 = axes[1, 1]
    ax4.scatter(dados["investimento"], dados["retorno"],
                s=120, c="#FF6B6B", alpha=0.7, edgecolors="black")
    ax4.set_xlabel("Investimento (R$)")
    ax4.set_ylabel("Retorno (R$)")
    ax4.set_title("Investimento × Retorno")
    ax4.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    plt.savefig(ARQUIVO_SAIDA, dpi=120, bbox_inches="tight")
    print(f"Dashboard salvo em: {ARQUIVO_SAIDA}")
    plt.show()


if __name__ == "__main__":
    criar_dashboard(gerar_dados())
