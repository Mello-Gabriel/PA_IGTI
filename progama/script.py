#%%
import glob
from funcao import nome_empresas, pdf_to_text, pegar_links, pegar_pdfs, wordcloud

#%%
pdfs=glob.glob('..\pdf_files\*.pdf')
if len(pdfs) == 0:
    nome_empresas()
    pegar_links()
    pegar_pdfs()
    [pdf_to_text(pdf) for pdf in pdfs]
    text=glob.glob('../text_files/*.*')
    [wordcloud(text) for file in text]

else:
    text=glob.glob('../text_files/*.*')
    [pdf_to_text(pdf) for pdf in pdfs if len(text)==0]
    tabelas=glob.glob('../tabela_palavras/*.*')
    [wordcloud(file) for file in text if len(tabelas)==0]
# %%
