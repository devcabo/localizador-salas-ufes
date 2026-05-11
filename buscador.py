import pandas as pd
import glob
import os

def agenda_sala_vaga():
    pasta_planilhas = "Planilhas"
    sala_alvo = input("Digite a sala: ").strip().upper()
    dia_semana = input("Qual dia da semana?: ").strip().capitalize()

    # Busca todos os arquivos Excel na subpasta especificada
    arquivos = glob.glob(os.path.join(pasta_planilhas, "*.xlsx"))
    
    for arquivo in arquivos:
        try:
            # Carrega planilha para identificar onde começa a tabela real
            df_bruto = pd.read_excel(arquivo, sheet_name='Resumo')
            
            # Localiza a linha de cabeçalho que contém 'Sala' e 'Horário'
            indice_cabecalho = 0
            for i, row in df_bruto.iterrows():
                if 'Sala' in row.values and 'Horário' in row.values:
                    indice_cabecalho = i
                    break
            
            # Recarrega os dados a partir da linha de cabeçalho detectada
            df = pd.read_excel(arquivo, sheet_name='Resumo', skiprows=indice_cabecalho + 1)
            df.columns = [str(c).strip() for c in df_bruto.iloc[indice_cabecalho].values]

            if 'Sala' in df.columns:
                # Preenche nomes das salas e limpa formatação (.0)
                df['Sala'] = df['Sala'].ffill().astype(str).str.replace('.0', '', regex=False).str.upper()
            
            # Filtra pela sala pesquisada
            dados_sala = df[df['Sala'].str.contains(sala_alvo, na=False)]
            
            if not dados_sala.empty:
                print(f"\n🏢 PRÉDIO: {os.path.basename(arquivo)}")
                
                for _, linha in dados_sala.iterrows():
                    horario = str(linha['Horário']).strip()
                    status_dia = linha[dia_semana]
                    
                    # Ignora linhas nulas de horário
                    if horario.lower() == 'nan':
                        continue

                    # Verifica disponibilidade baseada puramente na célula do dia
                    if pd.isna(status_dia):
                        print(f"   ✅ Livre: {horario}")
                    else:
                        print(f"   ❌ Ocupado ({horario}): {status_dia}")

        except Exception as e:
            print(f"⚠️ Erro no arquivo {os.path.basename(arquivo)}: {e}")

if __name__ == "__main__":
    agenda_sala_vaga()