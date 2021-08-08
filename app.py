from numpy.core.fromnumeric import size
import streamlit as st
from funcao import *
import plotly.express as px

#títulos do aplicativo
st.title('Meu primeiro app!') # principal
st.sidebar.title('Titulo da sidebar') # da sidebar

#captura o nome das empresas
empresas=nome_empresas()

#select box da empresa
empresa=st.sidebar.selectbox('Selecione a empresa', empresas)


#apresentar o WordCloud da empresa selecionada
st.image(fr'pic/{empresa}.png')

#apresentar o grafico com as palavras mais usadas
tabela=pd.read_csv(f'/tabela_palavras/{empresa}.csv', index_col=1).sort_values(by='quantidade',ascending=False)[:20]
fig= px.histogram(tabela, x=tabela.index, y='quantidade')
st.plotly_chart(fig)