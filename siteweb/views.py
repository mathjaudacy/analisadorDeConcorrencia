from django.shortcuts import render
from siteweb.core.raspagem import raspar_dados
from siteweb.core.rasparConc import raspagem_concorrentes
from siteweb.core.inteligencio import comparacaoIa
from siteweb.core.utils import ler_todas_lojas
#from utils.cache import salvar_cache, ler_cache
from siteweb.core.servicos import executar_raspagem
import json
from django.conf import settings

def home(request):
    return render(request, 'siteweb/index.html')

def raspar_loja(request):
    if request.method == 'POST':
        urlLoja = request.POST.get("urlLoja")
        nomeLoja = request.POST.get("nomeLoja")
        chave_cache = f"produtos:{nomeLoja}"
        produto = executar_raspagem(nomeLoja, urlLoja) #ler_cache(chave_cache)  
        print("Produtos: ",produto)

        return render(request, 'siteweb/detalhesLoja.html', {
            'loja': {'nome': nomeLoja, 'url':urlLoja, 'chave-cache':chave_cache},
            'produtos': produto
        })
    
def comparador(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            raspagem, arquivo = raspagem_concorrentes(dados)
            print(f"ARQUIVO: {arquivo}")
            print("Raspagem concorrente: \n", raspagem)
            comparacaoIa(arquivo)
            url_download = settings.MEDIA_URL + arquivo
            
            return render(request, "siteweb/comparador.html", {"comparacoes": raspagem,  "url_download": url_download})
        except json.JSONDecodeError:
                return render(request, "siteweb/comparador.html", {"erro": "Erro ao decodificar JSON"})
    else:
            return render(request, "siteweb/comparador.html", {"erro": "Método inválido"})

def lojas_salvas(request):
    lojas= ler_todas_lojas()
    return render(request, "siteweb/index.html", {"lojas":lojas})
