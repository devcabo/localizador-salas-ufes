# 🏢 Localizador de Salas Vagas - UFES

Este projeto é uma ferramenta desenvolvida em Python para facilitar a busca de salas disponíveis nos prédios da UFES, utilizando os arquivos de distribuição de salas (.xlsx) fornecidos pela faculdade.

O sistema analisa a aba "Resumo" das planilhas, identifica os horários ocupados e lista apenas os intervalos em que a sala pesquisada está livre.

## 🚀 Como Funciona
A ferramenta possui duas versões:
1. **Web (Streamlit):** Interface amigável onde você arrasta o arquivo Excel e consulta os horários no navegador.
2. **Local (Terminal):** Script Python para processar arquivos salvos em uma pasta local.

## 🛠️ Tecnologias Utilizadas
* [Python](https://www.python.org/) - Linguagem principal.
* [Pandas](https://pandas.pydata.org/) - Manipulação e análise de dados.
* [Streamlit](https://streamlit.io/) - Transformação do script em interface web.
* [Openpyxl](https://openpyxl.readthedocs.io/) - Leitura de arquivos Excel.

## 📂 Estrutura do Repositório
* `app.py`: Código fonte da interface Web.
* `buscador.py`: Código fonte para uso via terminal.
* `requirements.txt`: Lista de dependências para o servidor online.

## 💻 Como Rodar Localmente

1. Clone o repositório:
```bash
git clone [https://github.com/devcabo/localizador-salas-ufes.git](https://github.com/devcabo/localizador-salas-ufes.git)
```
2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
3. Para rodar a versão Web localmente:
```bash
streamlit run app.py
```
4. Para rodar a versão de terminal:
```bash
python buscador.py
```

Aproveite o projeto. :--)
