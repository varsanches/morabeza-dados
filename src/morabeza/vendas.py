"""Vendas da Morabeza em Python idiomático (Sessão 2).

Cada venda passa a ser um objeto Venda (dataclass) em vez de um dicionário.
Linhas com erros levantam VendaInvalida e são postas de parte na leitura.
"""
from __future__ import annotations

import csv
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date

ILHAS_SERVIDAS = {"Santiago", "São Vicente", "Sal", "Boa Vista", "Fogo", "Santo Antão"}


class VendaInvalida(Exception):
    """Uma linha do ficheiro de vendas não pode ser transformada numa Venda."""


@dataclass(frozen=True)
class Venda:
    venda_id: str
    data: date
    cliente_id: str
    ilha: str
    categoria: str
    quantidade: int
    preco_unitario: int

    @property
    def total(self) -> int:
        """Valor da venda em escudos."""
        return self.quantidade * self.preco_unitario


def criar_venda(linha: dict[str, str]) -> Venda:
    """Converte uma linha do CSV numa Venda, ou levanta VendaInvalida."""
    try:
        quantidade = int(linha["quantidade"])
        preco_unitario = int(linha["preco_unitario"])
        data = date.fromisoformat(linha["data"])
    except ValueError as erro:
        raise VendaInvalida(f"{linha['venda_id']}: valor impossível") from erro

    if quantidade <= 0 or preco_unitario <= 0:
        raise VendaInvalida(f"{linha['venda_id']}: quantidade e preço têm de ser maiores do que 0")
    if linha["ilha"] not in ILHAS_SERVIDAS:
        raise VendaInvalida(f"{linha['venda_id']}: ilha não servida")

    return Venda(
        venda_id=linha["venda_id"],
        data=data,
        cliente_id=linha["cliente_id"],
        ilha=linha["ilha"],
        categoria=linha["categoria"],
        quantidade=quantidade,
        preco_unitario=preco_unitario,
    )


def ler_vendas(caminho: str) -> Iterator[Venda]:
    """Gerador: devolve, uma a uma, as vendas válidas do ficheiro. As inválidas são ignoradas."""
    with open(caminho, newline="", encoding="utf-8") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            try:
                yield criar_venda(linha)
            except VendaInvalida:
                continue


def contar_invalidas(caminho: str) -> int:
    """Número de linhas do ficheiro que não dão uma Venda válida."""
    invalidas = 0
    with open(caminho, newline="", encoding="utf-8") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            try:
                criar_venda(linha)
            except VendaInvalida:
                invalidas += 1
    return invalidas


def vendas_acima(vendas: Iterable[Venda], limite: int) -> list[Venda]:
    """Vendas com total maior do que o limite, numa compreensão de lista."""
    return [v for v in vendas if v.total > limite]


def total_por(vendas: Iterable[Venda], chave: Callable[[Venda], str]) -> dict[str, int]:
    """Soma dos totais agrupada pela função chave. Ex.: total_por(vendas, lambda v: v.ilha)."""
    totais: dict[str, int] = {}
    for v in vendas:
        totais[chave(v)] = totais.get(chave(v), 0) + v.total
    return totais


# ---------------------------------------------------------------- Extensão (opcional)

def top_n(totais: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Os n pares (chave, total) com maior total, do maior para o menor."""
    # EXTENSÃO: sorted(totais.items(), key=lambda par: ..., reverse=True) e depois [:n]
    raise NotImplementedError("Extensão por fazer")


@contextmanager
def cronometro(nome: str):
    """Mede o tempo de um bloco. Uso: with cronometro("leitura"): ..."""
    # EXTENSÃO: guarda time.perf_counter() antes do yield e, num finally,
    #           imprime f"{nome}: {segundos:.3f} s".
    raise NotImplementedError("Extensão por fazer")
    yield
