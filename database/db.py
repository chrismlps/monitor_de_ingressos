import sqlite3
from datetime import datetime

BANCO = "database/precos.db"

def criar_tabelas():
    """
    Cria as tabelas no banco de dados se ainda não existirem.
    """
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coletas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            nome_evento TEXT,
            horario_coleta TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coleta_id INTEGER NOT NULL,
            setor TEXT NOT NULL,
            preco_texto TEXT NOT NULL,
            preco_valor REAL,
            FOREIGN KEY (coleta_id) REFERENCES coletas(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Banco de dados pronto!")


def salvar_coleta(dados: dict):
    """
    Salva os dados de uma coleta no banco.
    """
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO coletas (url, nome_evento, horario_coleta)
        VALUES (?, ?, ?)
    """, (dados["url"], dados["evento"], dados["horario_coleta"]))

    coleta_id = cursor.lastrowid

    for ingresso in dados["ingressos"]:
        try:
            preco_texto = ingresso["preco"]
            preco_valor = float(
                preco_texto
                .replace("A PARTIR DE R$", "")
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
        except:
            preco_valor = None

        cursor.execute("""
            INSERT INTO precos (coleta_id, setor, preco_texto, preco_valor)
            VALUES (?, ?, ?, ?)
        """, (coleta_id, ingresso["setor"], ingresso["preco"], preco_valor))

    conn.commit()
    conn.close()
    print(f"Coleta salva! ID: {coleta_id}")
    return coleta_id


def buscar_historico(url: str) -> list:
    """
    Retorna todo o histórico de preços de um evento.
    """
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.horario_coleta, p.setor, p.preco_valor
        FROM coletas c
        JOIN precos p ON p.coleta_id = c.id
        WHERE c.url = ?
        ORDER BY c.horario_coleta ASC
    """, (url,))

    rows = cursor.fetchall()
    conn.close()

    historico = []
    for row in rows:
        historico.append({
            "horario": row[0],
            "setor": row[1],
            "preco": row[2]
        })

    return historico


# Teste
if __name__ == "__main__":
    criar_tabelas()

    dados_teste = {
        "url": "https://cheers.com.br/evento/cupido-fdp-sexta-dos-solteiros-33006",
        "evento": "Cupido FDP! Sexta dos solteiros!",
        "horario_coleta": datetime.now().isoformat(),
        "ingressos": [
            {"setor": "Pista", "preco": "A PARTIR DE R$ 10,00"},
            {"setor": "Camarote", "preco": "A PARTIR DE R$ 60,00"}
        ]
    }

    salvar_coleta(dados_teste)

    historico = buscar_historico(dados_teste["url"])
    print("\nHistórico salvo:")
    for item in historico:
        print(f"  {item['horario']} | {item['setor']} | R$ {item['preco']}")