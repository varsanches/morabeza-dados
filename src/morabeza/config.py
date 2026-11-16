"""Leitura da configuração do projeto (Sessão 3)."""
from pathlib import Path

import yaml

CHAVES_OBRIGATORIAS = ("ficheiro_vendas", "moeda")


class ConfigInvalida(Exception):
    """O ficheiro de configuração não existe ou falta-lhe alguma chave obrigatória."""


def carregar_config(caminho: str) -> dict:
    """Lê o ficheiro YAML e devolve um dicionário com a configuração."""
    if not Path(caminho).exists():
        raise ConfigInvalida(f"Ficheiro de configuração não encontrado: {caminho}")

    with open(caminho, encoding="utf-8") as ficheiro:
        config = yaml.safe_load(ficheiro)

    em_falta = [chave for chave in CHAVES_OBRIGATORIAS if chave not in config]
    if em_falta:
        raise ConfigInvalida(f"Faltam chaves na configuração: {', '.join(em_falta)}")

    return config 
    
