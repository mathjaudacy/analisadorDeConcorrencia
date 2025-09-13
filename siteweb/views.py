from django.shortcuts import render
from siteweb.core.raspagem import raspar_dados
from siteweb.core.utils import ler_todas_lojas
#from utils.cache import salvar_cache, ler_cache
from siteweb.core.servicos import executar_raspagem
import json
import locale

def home(request):
    return render(request, 'siteweb/index.html')

def raspar_loja(request):
    if request.method == 'POST':
        urlLoja = request.POST.get("urlLoja")
        nomeLoja = request.POST.get("nomeLoja")
        chave_cache = f"produtos:{nomeLoja}"
        produtos = executar_raspagem(nomeLoja, urlLoja) #ler_cache(chave_cache)  
       
        return render(request, 'siteweb/detalhesLoja.html', {
            'loja': {'nome': nomeLoja, 'url':urlLoja, 'chave-cache':chave_cache},
            'produtos': produtos
        })
    
def detalhe_produto(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            print("Dados recebidos:", dados)
            return render(request, "siteweb/detalheProduto.html", {"itens":[dados]})
        except json.JSONDecodeError:
             return render(request, "siteweb/detalheProduto.html", {"erro": "Erro ao decodificar JSON"})
    else:
        return render(request, "siteweb/detalheProduto.html", {"erro": "Método inválido"})


def lojas_salvas(request):
    lojas= ler_todas_lojas()
    return render(request, "siteweb/index.html", {"lojas":lojas})
