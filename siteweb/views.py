from django.shortcuts import render
from siteweb.core.raspagem import raspar_dados
from siteweb.core.utils import ler_todas_lojas
from utils.cache import salvar_cache, ler_cache


def home(request):
    return render(request, 'siteweb/index.html')

def raspar_loja(request):
    if request.method == 'POST':
        urlLoja = request.POST.get("urlLoja")
        nomeLoja = request.POST.get("nomeLoja")
        chave_cache = f"produtos:{nomeLoja}"
        produtos = ler_cache(chave_cache)     
        if not produtos:
            produtos = raspar_dados(urlLoja) #função da raspagem
            salvar_cache(chave_cache, produtos)
        return render(request, 'siteweb/detalhesLoja.html', {
            'loja': {'nome': nomeLoja, 'url':urlLoja, 'chave-cache':chave_cache},
            'produtos': produtos
        })
    
def detalhe_produto(request):
    if request.method == 'GET':
        nomeLoja= request.GET.get("nomeLoja")
        urlLoja= request.GET.get("urlLoja")
        nomeProduto= request.GET.get("nome")
        preco= request.GET.get("preco")
        imagem= request.GET.get("imagem")
        itens = {
            "nomeLoja": nomeLoja,
            "urlLoja": urlLoja,
            "nomeProduto": nomeProduto,
            "preco": preco,
            "imagem": imagem
        }

        return render(request, "siteweb/detalheProduto.html", {"itens":[itens]})
    else:
        return render(request, "siteweb/detalheProduto.html", {"erro": "Método inválido"})


def lojas_salvas(request):
    lojas= ler_todas_lojas()
    return render(request, "siteweb/index.html", {"lojas":lojas})
