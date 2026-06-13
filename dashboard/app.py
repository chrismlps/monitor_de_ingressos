import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import buscar_historico, criar_tabelas
from scraper.cheers_scraper import scrape_cheers
from database.db import salvar_coleta
from ai.analyzer import analisar_precos

# Configuração da página
st.set_page_config(
    page_title="Monitor de Ingressos",
    page_icon="🎫",
    layout="centered"
)

st.title("🎫 Monitor de Preços de Ingressos")
st.caption("Acompanhe os preços de eventos universitários na Cheers")

# Campo para o usuário colar a URL
url = st.text_input(
    "Cole a URL do evento da Cheers:",
    placeholder="https://cheers.com.br/evento/nome-do-evento"
)

if url:
    # Botão para coletar novos dados
    if st.button("Coletar preços agora"):
        with st.spinner("Acessando o site..."):
            criar_tabelas()
            dados = scrape_cheers(url)
            salvar_coleta(dados)
            st.success(f"Dados coletados para: **{dados['evento']}**")

    # Busca o histórico do banco
    historico = buscar_historico(url)

    if historico:
        st.subheader("Histórico de Preços")

        # Transforma em DataFrame para exibir
        df = pd.DataFrame(historico)
        df.columns = ["Horário", "Setor", "Preço (R$)"]

        # Separa por setor e plota gráfico
        setores = df["Setor"].unique()
        for setor in setores:
            st.markdown(f"**{setor}**")
            df_setor = df[df["Setor"] == setor].copy()
            st.line_chart(df_setor.set_index("Horário")["Preço (R$)"])

        # Tabela completa
        st.subheader("Tabela de Coletas")
        st.dataframe(df, use_container_width=True)

        # Análise da IA
        st.subheader("Análise da IA")
        with st.spinner("Consultando IA..."):
            analise = analisar_precos(url)
        st.info(analise)

    else:
        st.warning("Nenhum dado encontrado. Clique em 'Coletar preços agora' para começar.")