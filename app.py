import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Salas UFES", layout="centered")

st.title("🏢 Localizador de Salas Vagas")
st.markdown("Arraste o arquivo Excel do prédio e selecione a sala desejada.")

# 1. Campo de Upload
arquivo_postado = st.file_uploader("Escolha o arquivo Excel", type=["xlsx"])

if arquivo_postado:
    try:
        # 2. Lógica para encontrar o cabeçalho (idêntica ao seu buscador.py)
        df_bruto = pd.read_excel(arquivo_postado, sheet_name='Resumo')
        
        indice_cabecalho = 0
        for i, row in df_bruto.iterrows():
            if 'Sala' in row.values and 'Horário' in row.values:
                indice_cabecalho = i
                break
        
        # 3. Carrega os dados reais
        df = pd.read_excel(arquivo_postado, sheet_name='Resumo', skiprows=indice_cabecalho + 1)
        df.columns = [str(c).strip() for c in df_bruto.iloc[indice_cabecalho].values]

        if 'Sala' in df.columns:
            # Limpeza e preenchimento das salas
            df['Sala'] = df['Sala'].ffill().astype(str).str.replace('.0', '', regex=False).str.upper()
            
            # Pega a lista de salas únicas para o usuário escolher
            # Remove valores nulos ou vazios da lista
            lista_salas = sorted([s for s in df['Sala'].unique() if s.lower() != 'nan' and s.strip() != ''])

            # 4. Interface de Seleção
            col1, col2 = st.columns(2)
            with col1:
                sala_selecionada = st.selectbox("Selecione a Sala", lista_salas)
            with col2:
                dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
                dia_semana = st.selectbox("Dia da Semana", dias)

            # 5. Filtro e Exibição dos Resultados
            if sala_selecionada:
                dados_sala = df[df['Sala'] == sala_selecionada]
                
                st.subheader(f"📅 Agenda: Sala {sala_selecionada} na {dia_semana}")
                
                for _, linha in dados_sala.iterrows():
                    horario = str(linha['Horário']).strip()
                    status_dia = linha[dia_semana]
                    
                    if horario.lower() == 'nan' or horario == '': 
                        continue

                    if pd.isna(status_dia):
                        st.success(f"✅ **Livre:** {horario}")
                    else:
                        st.error(f"❌ **Ocupado ({horario}):** {status_dia}")
        else:
            st.error("Não foi possível encontrar a coluna 'Sala' neste arquivo.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")