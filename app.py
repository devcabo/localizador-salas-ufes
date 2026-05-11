import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Buscador de Salas UFES", layout="wide")

st.title("🏢 Central de Salas UFES")
st.markdown("Arraste **um ou vários** arquivos Excel dos prédios para buscar.")

# 1. Upload de múltiplos arquivos
arquivos_postados = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

if arquivos_postados:
    todas_as_salas_data = {} # Dicionário para guardar os DataFrames de cada prédio

    for arquivo in arquivos_postados:
        try:
            df_bruto = pd.read_excel(arquivo, sheet_name='Resumo')
            
            # Encontra o cabeçalho
            indice_cabecalho = 0
            for i, row in df_bruto.iterrows():
                if 'Sala' in row.values and 'Horário' in row.values:
                    indice_cabecalho = i
                    break
            
            df = pd.read_excel(arquivo, sheet_name='Resumo', skiprows=indice_cabecalho + 1)
            df.columns = [str(c).strip() for c in df_bruto.iloc[indice_cabecalho].values]

            if 'Sala' in df.columns:
                df['Sala'] = df['Sala'].ffill().astype(str).str.replace('.0', '', regex=False).str.upper()
                # Guarda o DataFrame usando o nome do arquivo como chave
                todas_as_salas_data[arquivo.name] = df
        except Exception as e:
            st.error(f"Erro no arquivo {arquivo.name}: {e}")

    # 2. Criar lista de seleção única (Sala + Nome do Prédio)
    opcoes_selecao = []
    for nome_predio, df in todas_as_salas_data.items():
        salas_do_predio = df['Sala'].unique()
        for s in salas_do_predio:
            if str(s).lower() != 'nan' and str(s).strip() != '':
                # Formato: "105 | IC 2 - 2026.1.xlsx"
                opcoes_selecao.append(f"{s} | {nome_predio}")

    opcoes_selecao.sort()

    if opcoes_selecao:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            escolha = st.selectbox("Selecione a Sala e o Prédio", opcoes_selecao)
        with col2:
            dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
            dia_semana = st.selectbox("Dia da Semana", dias)

        # 3. Separar a escolha para buscar o dado correto
        sala_nome, predio_nome = escolha.split(" | ")
        df_selecionado = todas_as_salas_data[predio_nome]
        dados_sala = df_selecionado[df_selecionado['Sala'] == sala_nome]

        # 4. Exibição
        st.subheader(f"📍 {predio_nome} - Sala {sala_nome} ({dia_semana})")
        
        # Criar uma lista para exibir os horários de forma mais limpa em colunas ou cards
        for _, linha in dados_sala.iterrows():
            horario = str(linha['Horário']).strip()
            status_dia = linha[dia_semana]
            
            if horario.lower() == 'nan' or horario == '': continue

            if pd.isna(status_dia):
                st.success(f"✅ **Livre:** {horario}")
            else:
                st.error(f"❌ **Ocupado ({horario}):** {status_dia}")
    else:
        st.info("Aguardando upload de arquivos válidos...")
