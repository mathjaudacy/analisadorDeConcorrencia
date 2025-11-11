import json
from playwright.sync_api import sync_playwright
import random
import time

def raspar_dados(playwright, BASE_URL):
    browser = playwright.chromium.launch(headless=False)
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116 Safari/537.36"
    ]
    viewport={"width": 1280, "height": 800}
    context = browser.new_context(
        user_agent=random.choice(USER_AGENTS),
        viewport={"width":1280,"height":800}
    )
    page = context.new_page()
    print("[INFO] Acessando página...")
    page.goto(BASE_URL, timeout=50000)
    time.sleep(2)
    page.mouse.wheel(0, 1000)
    time.sleep(1)
    if "algo deu errado" in page.content():
        print("[ERRO] Página de erro detectada. Abortando raspagem.")
        browser.close()
        return []

    page.wait_for_selector('div.s-main-slot', timeout=15000)
    print("[INFO] Página carregada, buscando produtos...")

    product_cards = page.query_selector_all('div.s-main-slot div[data-asin]:not([data-asin=""])')
    print(f"[INFO] Total de blocos com data-asin: {len(product_cards)}")

    produtos = []
    for i, card in enumerate(product_cards, 1):
        asin = card.get_attribute('data-asin')
        if not asin:
            print(f"[SKIP] Produto {i} ignorado (ASIN vazio).")
            continue

        price_el = card.query_selector('span.a-price > span.a-offscreen')
        price = price_el.inner_text().strip() if price_el else None
        if not price:
            print(f"[SKIP] Produto {i} ignorado (preço não encontrado {price}).")
            continue
        print("Preço recebido:", {price})
        name_el = card.query_selector('div[data-cy="title-recipe"] a')
        
        linkProduto = "https://www.amazon.com.br" + name_el.get_attribute('href') if name_el else None
        if not linkProduto:
                print(f"[SKIP] Produto {i} ignorado (link não encontrado).")
                continue
        print("Link recebido:", {linkProduto})
        try:
            context = browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                locale="pt-BR")
            produto_page = context.new_page()
            produto_page.goto(linkProduto, timeout=60000)
            time.sleep(2)
            produto_page.mouse.wheel(0, 1000)
            time.sleep(1)
            produto_page.wait_for_selector("h1#title span#productTitle")
            nome_el = produto_page.query_selector("h1#title span#productTitle")
            if not nome_el:
                raise Exception("Titulo não encontrado")
            nome = nome_el.inner_text().strip() if nome_el else None
            if not nome or "hq" in nome.lower():
                continue

            nome_loja = produto_page.query_selector("span.offer-display-feature-text-message")
            nomeLoja = nome_loja.inner_text().strip() if nome_loja else None

            img_el = produto_page.query_selector("#imgTagWrapperId #landingImage")
            imagem = img_el.get_attribute("src") if img_el else None

            # Seleciona todas as linhas da tabela de especificações
            rows = produto_page.query_selector_all("table.a-normal tbody tr")

            for row in rows:
                try:
                    label_el = row.query_selector("td.a-span3 span.a-text-bold")
                    value_el = row.query_selector("td.a-span9 span.po-break-word")

                    label = label_el.inner_text().strip() if label_el else None
                    value = value_el.inner_text().strip() if value_el else None

                    if label and value:
                        nome += f"|{label}:{value}"
                except Exception as e:
                    print(f"Erro ao extrair especificação: {e}")
                    continue
            nome = f"{nomeLoja}|{nome}" if nomeLoja else nome

            print("Certo", nome)

            produtos.append({
                "asin": asin,
                "nome": nome,
                "preco": price,
                "imagem": imagem,
                "url": linkProduto
            })
            produto_page.close()  
        except Exception as e:
            print(f"Erro ao acessar {linkProduto}: {e}")
            continue

    print(f"[INFO] Total de produtos válidos encontrados: {len(produtos)}")

    with open("amazon_data.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

    browser.close()
    if(produtos == 1 or produtos == None or produtos == "" or produtos == 0 ):
        print(f"Numero de Produtos passados {produtos}")
        print("A raspagem houve um erro, sera refeita!")
        raspar_dados()
    return produtos
