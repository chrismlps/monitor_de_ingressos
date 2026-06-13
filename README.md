# Monitor de Ingressos

Sistema de acompanhamento e análise de preços de ingressos para eventos universitários, com integração de IA para gerar recomendações de compra/revenda, desenvolvido para a disciplina de Engenharia de Software.

## Funcionalidades

- **Web Scraping**: coleta automática de preços de eventos no site Cheers
- **Histórico de preços**: armazenamento em banco de dados SQLite
- **Análise com IA**: recomendações de compra/venda geradas pelo modelo Llama 3.3 70B via Groq
- **Dashboard**: interface visual com gráficos de histórico de preços

## Tecnologias

- **Python 3**
- **Playwright** — automação de navegador para scraping
- **SQLite** — armazenamento de dados
- **Groq API** (Llama 3.3 70B) — análise inteligente dos dados
- **Streamlit** — dashboard interativo

## Como executar

### 1. Pré-requisitos

- Python 3.10+ instalado
- Conta gratuita no [Groq](https://console.groq.com) para gerar uma API key

### 2. Configuração

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/chrismlps/monitor_de_ingressos.git
cd monitor_de_ingressos
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
playwright install chromium
```

Crie um arquivo `.env` na raiz do projeto com sua chave da Groq na seguinte estrutura:
GROQ_API_KEY=sua_chave_aqui

### 3. Executando

**Coleta via linha de comando:**

```bash
python main.py
```

**Dashboard interativo:**

```bash
streamlit run dashboard/app.py
```

## Estrutura do projeto

monitor_de_ingressos/

├── scraper/          # Coleta de dados do site Cheers

├── database/         # Armazenamento e consulta SQLite

├── ai/               # Integração com IA para análise

├── dashboard/         # Interface Streamlit

└── main.py           # Execução via linha de comando

## Limitações e trabalhos futuros

- Atualmente o monitoramento é manual (execução do `main.py`), futuramente poderia ser automatizado com agendadores como o APScheduler
- Não há monitoramento da revenda em redes sociais ou no site
- Dados coletados limitados
