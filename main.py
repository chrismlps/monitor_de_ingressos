from database.db import criar_tabelas, salvar_coleta
from scraper.cheers_scraper import scrape_cheers
from ai.analyzer import analisar_precos

# Lista de eventos para monitorar
EVENTOS = [
    "https://cheers.com.br/evento/cupido-fdp-sexta-dos-solteiros-33006",
    "https://cheers.com.br/evento/enigma-do-hexa-33115",
    "https://cheers.com.br/evento/calourada-da-odisseia-32510"
]

def main():
    print("🎫 Monitor de Ingressos — iniciando coleta\n")
    
    # Garante que o banco existe
    criar_tabelas()

    for url in EVENTOS:
        print(f"📡 Coletando: {url}")
        
        # Coleta os dados
        dados = scrape_cheers(url)
        print(f"   Evento: {dados['evento']}")
        for ingresso in dados['ingressos']:
            print(f"   {ingresso['setor']}: {ingresso['preco']}")

        # Salva no banco
        salvar_coleta(dados)
        print("   ✅ Salvo no banco")

        # Análise da IA
        print("   🤖 Analisando com IA...")
        analise = analisar_precos(url)
        print(f"\n   Análise:\n   {analise}\n")
        print("-" * 50)

    print("\n✅ Coleta finalizada!")

if __name__ == "__main__":
    main()