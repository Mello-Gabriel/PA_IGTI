import streamlit as st
import streamlit.components.v1 as components
from funcao import *
import plotly.express as px

palavras = as_palavras()

# layout da página
st.set_page_config(layout='wide')

# títulos do aplicativo
st.title('SUSTENTABILIDADE EMPRESARIAL')  # principal
st.subheader(
    'Conheça o relatório de sustentabilidade (2019) das empresas que estão na carteira ISE da B3.')
st.sidebar.title('Escolha as empresas')  # da sidebar


# captura o nome das empresas
empresas = nome_empresas()

# select box da empresa
empresa = st.sidebar.selectbox('Selecione a empresa principal', empresas)
empresa2 = st.sidebar.selectbox(
    'Selecione uma empresa para comparar', empresas)

# texto na side bar
st.sidebar.write(
    'Esse é um aplicativo web desenvolvido para conclusão do curso de MBA em Ciências de Dados do [IGTI](https://www.igti.com.br/pos-graduacao/ciencia-de-dados).')
st.sidebar.write(
    'Eu sou Gabriel de Mello, me conheça melhor em [LinkedIn](https://www.linkedin.com/in/gabriel-guimaraes-de-mello/).')
st.sidebar.write(
    'Esse projeto foi escrito em Python e está disponível no [Github](https://github.com/Mello-Gabriel/PA_IGTI).')

#seção para o aplicativo do PowerBI embeded
with st.expander('NAVEGADOR DE PALAVRAS E EMPRESAS'):
    st.write('Utilize essa rede de relacionamento para explorar as relações entre as empresas através das palavras de seus relatórios. As empresas são representadas pelos pontos coloridos e as palavras pelos pontos cinzas')
    st.write('Experimente utilizar a caixa da direta para buscar palavras relavantes e identificar as empresas que as utilizaram no relatório')
    components.iframe('https://app.powerbi.com/view?r=eyJrIjoiMWNiMzllYjktYzU5OC00NzM0LWIzYzEtNzRhYzViNDk0MDM3IiwidCI6IjYxYzM2ZWZhLTAwY2UtNDIyMi1iY2VmLWM3MmRiNTZhYWM0NyJ9&pageName=ReportSection', height=720)

#seção com duas colunas, para apresentar as empresas comparadas.
col1, col2 = st.columns(2)
with col1:
    # apresentar o WordCloud da empresa selecionada
    st.header(empresa.upper())
    st.image(fr'pic/{empresa}.png')
    # apresentar o grafico com as palavras mais usadas
    tabela = pd.read_csv(fr'tabela_palavras/{empresa}.csv', index_col=1).sort_values(by='quantidade', ascending=False)[:20]
    fig = px.histogram(tabela, x=tabela.index, y='quantidade')
    st.plotly_chart(fig)
    #apresentar a empresa com maior similaridade
    top1 = top_similares(palavras, empresa)
    st.write("A empresa que possui o relatório mais similar é:",
            top1[0][1].upper())
    #apresentar o link para download do relatório
    st.write(f'Faça o download do relatório de sustentabilidade da {empresa.upper()}  aqui: [link](https://raw.githubusercontent.com/Mello-Gabriel/PA_IGTI/master/pdf_files/{empresa.replace(" ","%20")}.pdf)')

with col2:
    st.header(empresa2.upper())
    # apresentar o WordCloud da empresa selecionada
    st.image(fr'pic/{empresa2}.png')
    # apresentar o grafico com as palavras mais usadas
    tabela = pd.read_csv(fr'tabela_palavras/{empresa2}.csv', index_col=1).sort_values(
        by='quantidade', ascending=False)[:20]
    fig = px.histogram(tabela, x=tabela.index, y='quantidade')
    st.plotly_chart(fig)
    #apresentar a empresa com maior similaridade
    top2 = top_similares(palavras, empresa2)
    st.write("A empresa que possui o relatório mais similar é:",
            top2[0][1].upper())
    #apresentar o link para download do relatório.
    st.write(
        f'Faça o download do relatório da sustentabilidade da {empresa2.upper()} aqui: [link](https://raw.githubusercontent.com/Mello-Gabriel/PA_IGTI/master/pdf_files/{empresa2.replace(" ","%20")}.pdf)'
            )