import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Salas UFES", layout="centered")

st.title("🏢 Localizador de Salas Vagas")
st.markdown("Arraste o arquivo Excel do prédio para verificar os horários livres.")

# 1. Campo para arrastar o arquivo (Uploader)
arquivo_postado = st.file_uploader("Escolha o arquivo Excel", type=["xlsx"])

if arquivo_postado:
    # 2. Configurações de busca
    col1, col2 = st.columns(2)
    with col1:
        sala_alvo = st.text_input("Número da Sala (ex: 105)").strip().upper()
    with col2:
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        dia_semana = st.selectbox("Dia da Semana", dias)

    if sala_alvo:
        try:
            # Lógica de leitura idêntica ao seu script
            df_bruto = pd.read_excel(arquivo_postado, sheet_name='Resumo')
            
            indice_cabecalho = 0
            for i, row in df_bruto.iterrows():
                if 'Sala' in row.values and 'Horário' in row.values:
                    indice_cabecalho = i
                    break
            
            df = pd.read_excel(arquivo_postado, sheet_name='Resumo', skiprows=indice_cabecalho + 1)
            df.columns = [str(c).strip() for c in df_bruto.iloc[indice_cabecalho].values]

            if 'Sala' in df.columns:
                df['Sala'] = df['Sala'].ffill().astype(str).str.replace('.0', '', regex=False).str.upper()
                
                # Filtragem
                dados_sala = df[df['Sala'].str.contains(sala_alvo, na=False)]
                
                if not dados_sala.empty:
                    st.subheader(f"📅 Agenda: Sala {sala_alvo} na {dia_semana}")
                    
                    for _, linha in dados_sala.iterrows():
                        horario = str(linha['Horário']).strip()
                        status_dia = linha[dia_semana]
                        
                        if horario.lower() == 'nan': continue

                        if pd.isna(status_dia):
                            st.success(f"✅ **Livre:** {horario}")
                        else:
                            st.error(f"❌ **Ocupado ({horario}):** {status_dia}")
                else:
                    st.warning(f"Sala {sala_alvo} não encontrada no arquivo.")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")