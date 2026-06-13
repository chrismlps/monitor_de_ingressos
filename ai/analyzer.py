import os
import sys
from dotenv import load_dotenv
from groq import Groq

# Carrega a chave do arquivo .env
load_dotenv()
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Adiciona o caminho raiz para importar o banco
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import buscar_historico

def analisar_precos(url: str) -> str:
    """
    Busca o histórico de preços do banco e pede uma análise para a IA.
    """
    historico = buscar_historico(url)

    if not historico:
        return "Nenhum dado encontrado para esse evento."

    # Monta um resumo do histórico para mandar para a IA
    resumo = ""
    for item in historico:
        resumo += f"- {item['horario']} | Setor: {item['setor']} | Preço: R$ {item['preco']}\n"

    prompt = f"""
Você é um assistente especialista em análise de preços de ingressos para eventos universitários no Brasil.

Abaixo está o histórico de preços coletados para um evento:

{resumo}

Com base nesses dados, responda em português:
1. Qual é a tendência de preço (subindo, estável ou caindo)?
2. Vale a pena comprar agora ou esperar?
3. Para quem quer revender, esse é um bom momento para comprar?

Seja direto e objetivo. Use no máximo 5 linhas.
"""

    resposta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return resposta.choices[0].message.content


if __name__ == "__main__":
    url = "https://cheers.com.br/evento/cupido-fdp-sexta-dos-solteiros-33006"
    analise = analisar_precos(url)
    print("\nAnálise da IA:")
    print(analise)