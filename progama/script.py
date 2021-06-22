#%%
import glob
from funcao import nome_empresas, pdf_to_text, pegar_links, pegar_pdfs, top_similares, indicar_palavra, wordcloud, sim_euclidiana, matriz_similaridade
import pandas as pd
#%%
empresas=nome_empresas()
pdfs=[pdf.split('\\')[-1].split('.')[0] for pdf in glob.glob(r'..\pdf_files\*.pdf')]
textos=[texto.split('\\')[-1].split('.')[0] for texto in glob.glob(r'..\text_files\*.txt')]
tabelas=[tabela.split('\\')[-1].split('.')[0] for tabela in glob.glob(r'..\tabela_palavras\*.csv')]
empresas_sem_pdf=[empresa for empresa in empresas if empresa not in pdfs]
empresas_sem_texto=[empresa for empresa in empresas if empresa not in textos]
empresas_sem_tabela=[empresa for empresa in empresas if empresa not in tabelas]
#%%
if len(empresas_sem_pdf) > 0:
    links=pegar_links(empresas_sem_pdf)
    pegar_pdfs(empresas_sem_pdf, links)
#%%
if len(empresas_sem_texto) >0:
    caminhos=[glob.glob(fr'../pdf_files/{empresa}.pdf') for empresa in empresas_sem_texto]
    [pdf_to_text(caminho[0]) for caminho in caminhos]

#%%
if len(empresas_sem_tabela) >0:
    textos=[glob.glob(fr'../text_files/{empresa}.txt') for empresa in empresas_sem_tabela]
    [wordcloud(text[0]) for text in textos]
# %%
dicio_palavras={}
palavras=glob.glob(r'..\tabela_palavras\*.csv')
for palavra in palavras:
    ler_tabela=pd.read_csv(palavra, index_col=1).drop(columns='Unnamed: 0')
    ler_tabela=ler_tabela.to_dict('dict')
    dicio_palavras[palavra.split('\\')[-1].split('.')[0]]=ler_tabela['quantidade']
# %%
sim_euclidiana(dicio_palavras,'weg','ccr')
# %%
matriz_similaridade(dicio_palavras)
# %%
top_similares(dicio_palavras,'ccr', n=2)

# %%
indicar_palavra(dicio_palavras,'weg')
# %%
