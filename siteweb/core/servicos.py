# siteweb/core/servicos.py
from playwright.sync_api import sync_playwright
from siteweb.core.raspagem import raspar_dados
from utils.cache import salvar_cache, ler_cache
from django.db import models
import json
from siteweb.models import Loja, Produto

def executar_raspagem(nomeLoja, urlLoja):
    print("// -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- //")
    print("INICIO RASPAGEM")
    chave_cache = f"loja:{nomeLoja}"
    #produtos = 
    produtos_json = ler_cache(chave_cache)
    produtos = json.loads(produtos_json) if produtos_json else []
    produtos = list(produtos)
    if not produtos:
        print("Produtos não encontrados no cache")
        loja = Loja.objects.filter(url=urlLoja).first()
        if loja:
            print("Loja encontrada.")
            produtos = Produto.objects.filter(loja_id = loja.id).all()

            if isinstance(produtos, models.QuerySet) and not produtos.exists():
                with sync_playwright() as playwright:
                    produtos = raspar_dados(playwright, urlLoja)
                    produto_list = [
                        {
                            "nome": p.nome,
                            "preco": float(p.preco),
                            #"imagem": p.imagem.url if p.imagem else None,
                            "loja": p.loja_id
                        }
                        for p in produtos
                    ]   
                    salvar_cache(chave_cache, json.dumps(produto_list))
                
            else:
                print("Produtos encontrados no DB: " , len(produtos))
                produto_list = [
                    {
                        "nome": p.nome,
                        "preco": float(p.preco),
                        #"imagem": p.imagem.url if p.imagem else None,
                        "loja": p.loja_id
                    }
                    for p in produtos
                ]
                salvar_cache(chave_cache, json.dumps(produto_list))
        else:
            produtos = None
            print("Loja não encontrada")
            with sync_playwright() as playwright:
                produtos = raspar_dados(playwright, urlLoja)
            
    else:
        print("Produtos encontrados no cache.")
    print("// -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- //")
    return produtos


