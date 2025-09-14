# Raspagem de concorrentes
import pandas as pd
import os
from datetime import datetime
def raspagem_concorrentes():
    raspagem = [
        {
            "principal": {
                "nome": "Liquidificador A",
                "preco": "R$ 473,00",
                "imagem": "...",
                "url": "..."
            },
            "concorrentes": [
                {"nome": "Concorrente 1", "preco": "R$ 459,00", "imagem": "...", "url": "..."},
                {"nome": "Concorrente 2", "preco": "R$ 470,00", "imagem": "...", "url": "..."}
            ]
        },
        {
            "principal": {
                "nome": "Liquidificador B",
                "preco": "R$ 399,00",
                "imagem": "...",
                "url": "..."
            },
            "concorrentes": [
                {"nome": "Concorrente 3", "preco": "R$ 389,00", "imagem": "...", "url": "..."}
            ]
        }
    ]


    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    linhas = []

    for bloco in raspagem:
        principal_nome = bloco["principal"]["nome"]
        for concorrente in bloco["concorrentes"]:
            linhas.append({
                "principal": principal_nome,
                "concorrente": concorrente["nome"]
            })

    df = pd.DataFrame(linhas)
    df = df.astype(str)  
    nome_arquivo = f"comparacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    caminho = os.path.join("media", nome_arquivo)
    os.makedirs("media", exist_ok=True)
    df.to_parquet(caminho, index=False, engine="pyarrow")
    
    return raspagem, nome_arquivo
