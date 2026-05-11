import streamlit as st
import pandas as pd
import re

# Configuração da página e layout do site
st.set_page_config(page_title="Buscador de Salas UFES", layout="wide")

st.title("🏢 Central de Salas UFES CCHN - 2026")
st.markdown("Arraste os arquivos Excel dos prédios para buscar.")

# Componente para upload de múltiplos arquivos .xlsx
arquivos_postados = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

if arquivos_postados:
    todas_as_salas_data = {}

    for arquivo in arquivos_postados:
        try:
            # Lê a aba Resumo de cada arquivo
            df_bruto = pd.read_excel(arquivo, sheet_name='Resumo')
            
            # Localiza dinamicamente em qual linha começa a tabela real
            indice_cabecalho = 0
            for i, row in df_bruto.iterrows():
                if 'Sala' in row.values and 'Horário' in row.values:
                    indice_cabecalho = i
                    break
            
            # Recarrega o DataFrame a partir do cabeçalho encontrado
            df = pd.read_excel(arquivo, sheet_name='Resumo', skiprows=indice_cabecalho + 1)
            df.columns = [str(c).strip() for c in df_bruto.iloc[indice_cabecalho].values]

            if 'Sala' in df.columns:
                # Preenche nomes das salas e limpa formatação numérica
                df['Sala'] = df['Sala'].ffill().astype(str).str.replace('.0', '', regex=False).str.upper()
                
                # Extrai apenas o nome do prédio (ex: IC 2) usando Regex
                busca_ic = re.search(r'IC\s?\d+', arquivo.name, re.IGNORECASE)
                if busca_ic:
                    nome_exibicao = busca_ic.group().upper()
                else:
                    nome_exibicao = arquivo.name.replace('.xlsx', '')
                
                # Armazena os dados processados no dicionário
                todas_as_salas_data[nome_exibicao] = df
        except Exception as e:
            st.error(f"Erro no arquivo {arquivo.name}: {e}")

    # Monta a lista de opções para o menu de seleção (Sala | Prédio)
    opcoes_selecao = []
    for nome_predio, df in todas_as_salas_data.items():
        salas_do_predio = df['Sala'].unique()
        for s in salas_do_predio:
            if str(s).lower() != 'nan' and str(s).strip() != '':
                opcoes_selecao.append(f"{s} | {nome_predio}")

    opcoes_selecao.sort()

    if opcoes_selecao:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            escolha = st.selectbox("Selecione a Sala e o Prédio", opcoes_selecao)
        with col2:
            # Lista de dias úteis da semana
            dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
            dia_semana = st.selectbox("Dia da Semana", dias)

        # Separa a string selecionada para buscar o DataFrame correto
        sala_nome, predio_nome = escolha.split(" | ")
        df_selecionado = todas_as_salas_data[predio_nome]
        dados_sala = df_selecionado[df_selecionado['Sala'] == sala_nome]

        st.subheader(f"📍 {predio_nome} - Sala {sala_nome} ({dia_semana})")
        
        # Varre as linhas da sala para verificar disponibilidade
        for _, linha in dados_sala.iterrows():
            horario = str(linha['Horário']).strip()
            status_dia = linha[dia_semana]
            
            if horario.lower() == 'nan' or horario == '': continue

            # Exibe em verde se livre (NaN) ou vermelho se houver aula/evento
            if pd.isna(status_dia):
                st.success(f"✅ **Livre:** {horario}")
            else:
                st.error(f"❌ **Ocupado ({horario}):** {status_dia}")
    else:
        st.info("Aguardando upload de arquivos válidos...")

# Rodapé de créditos corrigido
st.divider()
st.markdown("<center><b>@devcabo</b></center>", unsafe_allow_html=True)
