from django.http import JsonResponse
from utils.cache import salvar_cache, ler_cache
import json
import redis

r=redis.Redis(host='localhost', port=6379, db=0)

def salvar_loja(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            nome = dados.get('nome')
            url = dados.get('url')
            chave_cache = f"loja:{nome}" 

            salvar_cache(chave_cache, {
                "nome": nome,
                "url": url
            })
           #Jonatas - Vai salvar no banco de dados'
            print(f"Loja recebida: {nome} - {url}")

            return JsonResponse({'mensagem': 'Loja salva com sucesso!'})
        except Exception as e:
            return JsonResponse({'mensagem': f'Erro ao salvar loja: {str(e)}'}, status=400)
    else:
        return JsonResponse({'mensagem': 'Método não permitido'}, status=405)
    
def ler_todas_lojas():
    lojas=[]

    for chave in r.scan_iter("loja:*"):
        valor = r.get(chave)
        if valor:
            try:
                loja=json.loads(valor)
                lojas.append(loja)
            except json.JSONDecodeError:
                pass
    return lojas