# siteweb/core/servicos.py
from playwright.sync_api import sync_playwright
from siteweb.core.raspagem import raspar_dados
from utils.cache import salvar_cache, ler_cache

def executar_raspagem(nomeLoja, urlLoja):
    chave_cache = f"loja:{nomeLoja}"
    produtos = ler_cache(chave_cache)
    if not produtos:
        with sync_playwright() as playwright:
            produtos = raspar_dados(playwright, urlLoja)
        salvar_cache(chave_cache, produtos)
    return produtos
