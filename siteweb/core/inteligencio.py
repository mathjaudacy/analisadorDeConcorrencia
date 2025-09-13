import pandas as pd
import ollama

# Exemplo de DataFrame
df = pd.DataFrame({
    "text": [
        "Este produto está sendo vendido por R$ 199,90 na loja oficial.",
        "Promoção: apenas R$ 59,99 até o fim do mês!",
        "Preço sugerido: R$ 349,00 ou 10x sem juros."
    ]
})

# Função para chamar o Ollama
def extrair_preco(texto):
    try:
        prompt = f"Texto: {texto}\n\nPergunta: Qual o preço do produto?"
        response = ollama.chat(
            model="gpt-oss:20b",  # aqui você coloca o modelo disponível no seu Ollama
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        return f"Erro: {e}"

# Iterar sobre a coluna e salvar as respostas
df["preco"] = df["text"].apply(extrair_preco)

print(df)