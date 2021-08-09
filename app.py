import streamlit as st
from funcao import *
import plotly.express as px

palavras=as_palavras()

#layout da página
st.set_page_config(layout='wide')

#títulos do aplicativo
st.title('SUSTENTABILIDADE EMPRESARIAL') # principal
st.subheader('Conheça o relatório de sustentabilidade (2019) das empresas que estão na carteira ISE da B3.')
st.sidebar.title('Escolha as empresas') # da sidebar


#captura o nome das empresas
empresas=nome_empresas()

#select box da empresa
empresa=st.sidebar.selectbox('Selecione a empresa principal', empresas)
empresa2=st.sidebar.selectbox('Selecione uma empresa para comparar', empresas)

#texto na side bar
st.sidebar.write('Esse é um aplicativo web desenvolvido para conclusão do curso de MBA em Ciências de Dados do [IGTI](https://www.igti.com.br/pos-graduacao/ciencia-de-dados).')
st.sidebar.write('Eu sou Gabriel de Mello, me conheça melhor em [LinkedIn](https://www.linkedin.com/in/gabriel-guimaraes-de-mello/).')
st.sidebar.write('Esse projeto foi escrito em Python e está disponível no [Github](https://github.com/Mello-Gabriel/PA_IGTI).')

st.write(sim_euclidiana(palavras, empresa,empresa2))

col1, col2 = st.columns(2)
with col1:
    st.header(empresa.upper())#apresentar o WordCloud da empresa selecionada
    st.image(fr'pic/{empresa}.png')
    #apresentar o grafico com as palavras mais usadas
    tabela=pd.read_csv(fr'tabela_palavras/{empresa}.csv', index_col=1).sort_values(by='quantidade',ascending=False)[:20]
    fig= px.histogram(tabela, x=tabela.index, y='quantidade')
    st.plotly_chart(fig)
    top1=top_similares(palavras, empresa)
    st.write("A empresa que possui o relatório mais similar é:", top1[0][1].upper())
    st.write(f'Faça o download do relatório de sustentabilidade da {empresa.upper()}  aqui: [link](https://raw.githubusercontent.com/Mello-Gabriel/PA_IGTI/master/pdf_files/{empresa.replace(" ","%20")}.pdf)')


with col2:
    st.header(empresa2.upper())
    #apresentar o WordCloud da empresa selecionada
    st.image(fr'pic/{empresa2}.png')
    #apresentar o grafico com as palavras mais usadas
    tabela=pd.read_csv(fr'tabela_palavras/{empresa2}.csv', index_col=1).sort_values(by='quantidade',ascending=False)[:20]
    fig= px.histogram(tabela, x=tabela.index, y='quantidade')
    st.plotly_chart(fig)
    top2=top_similares(palavras, empresa2)
    st.write("A empresa que possui o relatório mais similar é:", top2[0][1].upper())
    st.write(f'Faça o download do relatório da sustentabilidade da {empresa2.upper()} aqui: [link](https://raw.githubusercontent.com/Mello-Gabriel/PA_IGTI/master/pdf_files/{empresa2.replace(" ","%20")}.pdf)')

st.write(sim_euclidiana(palavras, empresa,empresa2))