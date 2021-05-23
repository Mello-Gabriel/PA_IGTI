# %%
import pandas as pd
from googlesearch import search
import requests
import glob
import PyPDF2
from wordcloud import WordCloud, STOPWORDS

# %%
def nome_empresas():
    with open(r'..\ref\empresas.txt','r', encoding='utf-8') as texto:
        global empresas
        empresas=texto.readlines()  
        empresas=[x.replace('\n','').lower() for x in empresas]
# %%
def pegar_links(ano='2019', numero='10'):
    global links
    links={}
    for empresa in empresas:
        links[empresa]=pd.DataFrame(search(f'{empresa} relatório sustentabilidade {ano} filetype:pdf', num_results=10))
    links=pd.concat(links).droplevel(1)
# %%
def pegar_pdfs():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    for empresa in empresas:
        try:
            r=requests.get(f"{links[empresa][0]}", allow_redirects=True, headers=headers)
            open(f'../pdf_files/{empresa}.pdf','wb').write(r.content)
        except:
            print(f"Não foi possível baixar o link {links[empresa][0]}")
#%%
def pdf_to_text(pdf_path):
    pdf_file=open(f'{pdf_path}', 'rb')
    pdf_reader=PyPDF2.PdfFileReader(pdf_file)
    num_pag=pdf_reader.numPages
    dici={}
    separador=" "
    for page in range(0, num_pag):
        pdf_pag=pdf_reader.getPage(page)
        pdf_text=pdf_pag.extractText().lower()
        replace_dict={
            '\n':' ',
            '- ':'',
            '˜ ':'fi',
            ' -':'',
            '%':'% ',
            "^\d+$":' ',
            '  ':' ',
            '˜':'fi'
            }
### Essa limpeza pode melhorar - talvez para retirar todos os caractéres que não sejam letras
        for x, y in replace_dict.items():
            pdf_text=pdf_text.replace(x,y)
        dici[page]=pdf_text
    lista="".join(dici.values())
    nome_arquivo=pdf_path.split("\\")[-1].split('.')[-2]
    f=open(f'../text_files/{nome_arquivo}.txt','w', encoding='utf-8')
    f.write(lista)
    f.close()    
    pdf_file.close()
    return(lista)
#%%
def wordcloud(text_path):
    texto=open(f'{text_path}', encoding='utf-8').read()
    stopwords=set(STOPWORDS)
    stopwords= set(STOPWORDS)
    new_words = []
    with open(r"..\ref\stopwords.txt", 'r', encoding='utf-8') as f:
      [new_words.append(word) for line in f for word in line.split()]
    new_stopwords = stopwords.union(new_words)
    wc=WordCloud(stopwords=new_stopwords).generate(texto)
    palavras=wc.process_text(texto)
    palavras=pd.DataFrame.from_dict(palavras, orient='index')
    palavras.sort_values(ascending=False, by=0,inplace=True)
    palavras.reset_index(inplace=True)
    palavras.columns=('palavras','quantidade')
    nome_arquivo=text_path.split("\\")[-1].split('.')[-2]
    palavras.to_csv(f'../tabela_palavras/{nome_arquivo}.csv')

# %%

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
