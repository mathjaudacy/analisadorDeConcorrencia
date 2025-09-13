from django.http import JsonResponse
from utils.cache import salvar_cache, ler_cache, apagar_cache
from siteweb.models import Loja
import json
import redis

r=redis.Redis(host='localhost', port=6379, db=0)

def salvar_loja(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            nome = dados.get('nome')
            url = dados.get('url')
            lojas = Loja.objects.filter(url=url)
            if lojas == "" or lojas== null or lojas==0:
                nova_loja = Loja(nome=nome, url=url)
                nova_loja.save() 
                print(f"Loja recebida: {nome} - {url}")
                return JsonResponse({'mensagem': 'Loja salva com sucesso!'})
            else:
                print("Loja ja existente.")
        except Exception as e:
            return JsonResponse({'mensagem': f'Erro ao salvar loja: {str(e)}'}, status=400)
    else:
        return JsonResponse({'mensagem': 'Método não permitido'}, status=405)
    


def ler_todas_lojas():
    lojas=[]

    for loja in Loja.objects.all():
       lojas.append({
            'keyLoja': loja.keyLoja,
            'nome': loja.nome,
            'url': loja.url
       })
    return lojas

def recarregar_prod(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            nome = dados.get('nome')
            url = dados.get('url')
            chave_cache = f"loja:{nome}" 

            apagar_cache(chave_cache)
            from siteweb.core.servicos import executar_raspagem
            executar_raspagem(nome, url)

            return JsonResponse({'mensagem': 'Cache apagado com sucesso!'})
        except Exception as e:
            return JsonResponse({'mensagem': f'Erro ao apagar cache: {str(e)}'}, status=400)
    else:
        return JsonResponse({'mensagem': 'Método não permitido'}, status=405)