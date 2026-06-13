from playwright.sync_api import sync_playwright
from datetime import datetime
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import criar_tabelas, salvar_coleta

def scrape_cheers(url: str) -> dict:
    """
    Acessa a página de um evento na Cheers e extrai os setores e preços.
    Suporta dois formatos: setores (Pista/Camarote) e ingresso único.
    """
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        print(f"Acessando: {url}")
        pagina.goto(url, wait_until="networkidle")

        # Extrai o nome do evento
        try:
            nome_evento = pagina.inner_text("h1")
        except:
            nome_evento = "Nome não encontrado"

        ingressos = []

        # Formato 1: setores separados (ex: Pista, Camarote)
        setores = pagina.query_selector_all("section[aria-labelledby^='event-v2-batch-group-']")
        for setor in setores:
            try:
                nome_setor = setor.query_selector("span[id^='event-v2-batch-group-']").inner_text()
                preco = setor.query_selector("div[id^='badge-component-event-v2-batch-group-']").inner_text()
                ingressos.append({
                    "setor": nome_setor,
                    "preco": preco
                })
            except:
                continue

        # Formato 2: ingresso único (sem setores)
        if not ingressos:
            try:
                # Pega todos os blocos de ingresso individual
                blocos = pagina.query_selector_all("section[id^='event-v2-batches'] div.flex.flex-col")
                for bloco in blocos:
                    try:
                        nome_setor = bloco.query_selector("p, span, h3").inner_text().strip()
                        preco_elemento = bloco.query_selector("[class*='price'], [class*='preco']")
                        if preco_elemento:
                            preco = preco_elemento.inner_text().strip()
                            ingressos.append({
                                "setor": nome_setor,
                                "preco": preco
                            })
                    except:
                        continue
            except:
                pass

        # Formato 3: busca pelo texto do preço diretamente
        if not ingressos:
            try:
                texto_completo = pagina.inner_text("body")
                linhas = texto_completo.split("\n")
                for i, linha in enumerate(linhas):
                    if "R$" in linha and "taxa" not in linha.lower() and "economiza" not in linha.lower():
                        # Procura o nome nas linhas anteriores, pulando linhas vazias
                        nome_setor = "Ingresso"
                        for j in range(i - 1, max(i - 5, 0), -1):
                            candidato = linhas[j].strip()
                            if candidato and candidato != "Ingressos" and len(candidato) < 60:
                                nome_setor = candidato
                                break
                        ingressos.append({
                            "setor": nome_setor,
                            "preco": linha.strip()
                        })
            except:
                pass

        navegador.close()

    resultado = {
        "url": url,
        "evento": nome_evento,
        "horario_coleta": datetime.now().isoformat(),
        "ingressos": ingressos
    }

    return resultado


if __name__ == "__main__":
    url_teste = "https://cheers.com.br/evento/enigma-do-hexa-33115"

    criar_tabelas()
    dados = scrape_cheers(url_teste)
    print(json.dumps(dados, indent=2, ensure_ascii=False))
    salvar_coleta(dados)