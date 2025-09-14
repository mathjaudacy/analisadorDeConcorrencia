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
    viewport={"width": 1280, "height": 800},
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

        name_el = card.query_selector('div[data-cy="title-recipe"] a')
        if not name_el:
            name_el = card.query_selector('h2 a')
        name = name_el.inner_text().strip() if name_el else None

        if not name:
            print(f"[SKIP] Produto {i} ignorado (sem nome).")
            continue

        price_el = card.query_selector('span.a-price > span.a-offscreen')
        price = price_el.inner_text().strip() if price_el else None

        link = "https://www.amazon.com.br" + name_el.get_attribute('href') if name_el else None

        # NOVO: Captura da imagem
        img_el = card.query_selector('.s-product-image-container img')
        image_url = img_el.get_attribute('src') if img_el else None

        print(f"[OK]Imagem: {img_el}")

        produtos.append({
            "asin": asin,
            "nome": name,
            "preco": price,
            "url": link,
            "imagem": image_url,
        })

    print(f"[INFO] Total de produtos válidos encontrados: {len(produtos)}")

    with open("amazon_data.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

    browser.close()
    return produtos
