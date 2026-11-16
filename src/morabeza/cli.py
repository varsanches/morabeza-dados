"""Linha de comandos do projeto Morabeza (Sessão 3).

Uso:  python -m morabeza.cli --ilha Sal
"""
import argparse
import logging
import sys

from morabeza.apoio import faturacao_por_ilha, ler_vendas
from morabeza.config import carregar_config

logger = logging.getLogger(__name__)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resumo de vendas da Morabeza")
    parser.add_argument("--config", default="config.yaml", help="ficheiro de configuração (por defeito: config.yaml)")
    parser.add_argument("--ilha", help="mostra só a faturação desta ilha")
    return parser

def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = criar_parser().parse_args(argv)

    config = carregar_config(args.config)
    caminho = config["ficheiro_vendas"]
    vendas = ler_vendas(caminho)
    logger.info("Li %d vendas de %s", len(vendas), caminho)

    por_ilha = faturacao_por_ilha(vendas)
    moeda = config["moeda"]
    if args.ilha is None:
        print(f"Faturação total: {sum(por_ilha.values())} {moeda}")
    elif args.ilha in por_ilha:
        print(f"Faturação em {args.ilha}: {por_ilha[args.ilha]} {moeda}")
    else:
        logger.error("Ilha desconhecida: %s", args.ilha)
        return 1
    return 0
 

if __name__ == "__main__":
    sys.exit(main())
