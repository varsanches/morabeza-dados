"""Resumo das vendas da Morabeza Distribuição (Sessão 1).

Lê um ficheiro CSV de vendas e mostra a faturação total e por ilha.
Só usa a biblioteca padrão do Python: o pandas chega na Sessão 4.
"""
import csv
import sys


def ler_vendas(caminho: str) -> list[dict]:
    """Lê o CSV de vendas e devolve uma lista de dicionários, um por venda.

    O módulo csv lê tudo como texto. As colunas quantidade e preco_unitario
    têm de ser convertidas para int, senão as contas dão resultados errados.
    """
    vendas = []
    with open(caminho, encoding="utf-8") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            linha["quantidade"] = int(linha["quantidade"])
            linha["preco_unitario"] = int(linha["preco_unitario"])
            vendas.append(linha)
    return vendas


def total_venda(venda: dict) -> int:
    """Valor de uma venda em escudos: quantidade vezes preço unitário."""
    return venda["quantidade"] * venda["preco_unitario"]


def faturacao_total(vendas: list[dict]) -> int:
    """Soma do valor de todas as vendas."""
    total = 0
    for venda in vendas:
        total += total_venda(venda)
    return total


def faturacao_por_ilha(vendas: list[dict]) -> dict[str, int]:
    """Dicionário {ilha: faturação} com a soma das vendas de cada ilha."""
    por_ilha = {}
    for venda in vendas:
        ilha = venda["ilha"]
        por_ilha[ilha] = por_ilha.get(ilha, 0) + total_venda(venda)
    return por_ilha


def ilha_top(por_ilha: dict[str, int]) -> str:
    """Nome da ilha com maior faturação."""
    return max(por_ilha, key=por_ilha.get)


# ---------------------------------------------------------------- Extensão (opcional)

def faturacao_mensal(vendas: list[dict]) -> dict[str, int]:
    """Dicionário {"AAAA-MM": faturação}, ordenado por mês."""
    por_mes = {}
    for venda in vendas:
        mes = venda["data"][:7]
        por_mes[mes] = por_mes.get(mes, 0) + total_venda(venda)
    return dict(sorted(por_mes.items()))


def formatar_cve(valor: int) -> str:
    """Formata um valor em escudos com espaço a separar os milhares: 1530740 -> '1 530 740 CVE'."""
    return f"{valor:,}".replace(",", " ") + " CVE"


# ---------------------------------------------------------------- Programa principal

def main(argv: list[str]) -> None:
    if len(argv) != 2:
        print("Uso: python -m morabeza.resumo <ficheiro.csv>")
        sys.exit(1)

    caminho = argv[1]
    vendas = ler_vendas(caminho)
    por_ilha = faturacao_por_ilha(vendas)

    print(f"Resumo de vendas: {caminho}")
    print(f"Número de vendas: {len(vendas)}")
    print(f"Faturação total: {formatar_cve(faturacao_total(vendas))}")
    print("Faturação por ilha:")
    for ilha, valor in sorted(por_ilha.items(), key=lambda par: par[1], reverse=True):
        print(f"  {ilha}: {formatar_cve(valor)}")
    print(f"Ilha com maior faturação: {ilha_top(por_ilha)}")
    print("Faturação por mês:")
    for mes, valor in faturacao_mensal(vendas).items():
        print(f"  {mes}: {formatar_cve(valor)}")


if __name__ == "__main__":
    main(sys.argv)
