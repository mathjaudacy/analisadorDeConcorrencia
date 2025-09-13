import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def salvar_cache(chave, dados, expira_em_segundos=5500):
    r.setex(chave, expira_em_segundos, json.dumps(dados))
    
def ler_cache(chave):
    valor = r.get(chave)
    return json.loads(valor) if valor else None
