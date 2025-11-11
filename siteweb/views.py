from django.shortcuts import render
from siteweb.core.raspagem import raspar_dados
from siteweb.core.rasparConc import raspagem_concorrentes
from siteweb.core.inteligencio import comparacaoIa
from siteweb.core.utils import ler_todas_lojas
#from utils.cache import salvar_cache, ler_cache
from siteweb.core.servicos import executar_raspagem
from siteweb.core.servicos import rankeador
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
            produto = dados["produtos"]
            numPages = dados["numPages"]
            nivelCompat = dados["nivelCompat"]
            raspagem, arquivo = raspagem_concorrentes(produto,numPages)
            print(f"ARQUIVO: {arquivo}")
            print("Foram encontrados:", len(raspagem[0]), "produtos concorrentes.\n")
            destinos = comparacaoIa(arquivo, nivelCompat)
            destino_nao = destinos[0]
            destino_sim = destinos[1]
            resultados_sim = destinos[2]
            resultadoRanking, texto = rankeador(resultados_sim)
            
            
            return render(request, "siteweb/comparador.html", {"comparacoes": raspagem, "destino_nao": destino_nao, "destino_sim": destino_sim, "resultados_ranking":resultadoRanking, "texto":texto, "dadosComparacao":resultados_sim})
        except json.JSONDecodeError:
                return render(request, "siteweb/comparador.html", {"erro": "Erro ao decodificar JSON"})
    else:
            return render(request, "siteweb/comparador.html", {"erro": "Método inválido"})

def lojas_salvas(request):
    lojas= ler_todas_lojas()
    return render(request, "siteweb/index.html", {"lojas":lojas})
