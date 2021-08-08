#%%
import pandas as pd
from googlesearch import search
import requests
import PyPDF2
from wordcloud import WordCloud, STOPWORDS
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from math import sqrt

# %%
def nome_empresas():
    with open('../ref/empresas.txt','r', encoding='utf-8') as texto:
        empresas=texto.readlines()  
        empresas=[x.replace('\n','').lower() for x in empresas]
        return empresas
# %%
def pegar_links(empresas, ano='2019', numero='10'):
    links={}
    if type(empresas) == list:
        for empresa in empresas:
            links[empresa]=pd.DataFrame(search(f'{empresa} relatório sustentabilidade {ano} filetype:pdf', num_results=10))
    else:
        links[empresas]=pd.DataFrame(search(f'{empresas} relatório sustentabilidade {ano} filetype:pdf', num_results=10))
    return links
# %%
def pegar_pdfs(empresas, links):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    for empresa in empresas:
        try:
            r=requests.get(f"{links[empresa][0][0]}", allow_redirects=True, headers=headers)
            open(f'../pdf_files/{empresa}.pdf','wb').write(r.content)
        except:
            print(f"Não foi possível baixar o link {links[empresa][0]}")
#%%
def pdf_to_text(caminho):
    pdf_file=open(caminho, 'rb')
    pdf_reader=PyPDF2.PdfFileReader(pdf_file)
    num_pag=pdf_reader.numPages
    dici={}
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
    nome_arquivo=caminho.split("/")[-1].split('.')[-2]
    f=open(f'../text_files/{nome_arquivo}.txt','w', encoding='utf-8')
    f.write(lista)
    f.close()    
    pdf_file.close()
    return(lista)
#%%
def wordcloud(text_path):
    texto=open(f'{text_path}', encoding='utf-8').read()
    stopwords=set(STOPWORDS)
    new_words = []
    with open("../ref/stopwords.txt", 'r', encoding='utf-8') as f:
      [new_words.append(word) for line in f for word in line.split()]
    new_stopwords = stopwords.union(new_words)
    wc=WordCloud(background_color='Black', stopwords=new_stopwords, min_font_size=3, width=1920, height=1080, colormap='viridis',collocation_threshold=10).generate(texto)
    palavras=wc.process_text(texto)
    palavras=pd.DataFrame.from_dict(palavras, orient='index')
    palavras.sort_values(ascending=False, by=0,inplace=True)
    palavras.reset_index(inplace=True)
    palavras.columns=('palavras','quantidade')
    nome_arquivo=text_path.split("/")[-1].split('.')[-2]
    palavras.to_csv(f'../tabela_palavras/{nome_arquivo}.csv')
    wc.to_file(f'../pic/{nome_arquivo}.png')
# %%
def sim_euclidiana(avaliacoes, c1, c2):
    mesmos_filmes = {}
    
    for filme in avaliacoes[c1]:
        if filme in avaliacoes[c2]:
            mesmos_filmes[filme] = 1
    
    if len(mesmos_filmes) == 0: return 0
    
    dist_euclidiana = sqrt(sum([pow((avaliacoes[c1][filme] - avaliacoes[c2][filme]),2) for filme in mesmos_filmes]))
    
    return 1 / (1 + dist_euclidiana)
#%%
def top_similares(avaliacoes, pessoa, n = 1, medida = sim_euclidiana):
    valores = [(medida(avaliacoes, pessoa, outra), outra) for outra in avaliacoes if outra != pessoa]
    valores.sort()
    valores.reverse()
    return valores[0:n]
#%%
def indicar_palavra(avaliacoes,pessoa):
    pessoa_similar=top_similares(avaliacoes, pessoa, 1)[0][1]
    recomendado=[]
    filme_pessoa=list(avaliacoes[pessoa].keys())
    filme_pessoa_similar=list(avaliacoes[pessoa_similar].keys())
    for filme in filme_pessoa_similar:
        if filme not in filme_pessoa:
            recomendado.append(filme)
    avaliacoes_df=pd.DataFrame.from_dict(avaliacoes)
    avaliacoes_df_recomendado=avaliacoes_df[avaliacoes_df.index.isin(recomendado)]
    avaliacoes_df_recomendado['sum']=avaliacoes_df_recomendado.sum(axis=1)
    return avaliacoes_df_recomendado['sum'].idxmax()
#%%
def matriz_similaridade(avaliacoes):
    matriz={}
    for usuariox in avaliacoes.keys():
        matriz[usuariox]={}
        for usuarioy in avaliacoes.keys():
            matriz[usuariox][usuarioy]=sim_euclidiana(avaliacoes,usuariox,usuarioy)
    matriz_df=pd.DataFrame.from_dict(matriz)
    np_matriz=matriz_df.to_numpy()
    Z = hierarchy.linkage(np_matriz, 'single')
    plt.figure()
    dn = hierarchy.dendrogram(Z, labels=list(matriz_df.columns), leaf_rotation=90)