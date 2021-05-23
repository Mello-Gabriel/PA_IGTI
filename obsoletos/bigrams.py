import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import nltk
from nltk import bigrams
from nltk.corpus import stopwords
import re
import networkx as nx
import warnings

warnings.filterwarnings('ignore')

sns.set(font_scale=1.5)
sns.set_style('whitegrid')

relatorio=open('./CCR_R.csv').read()

palavras=[relatorio.lower().split() for words in relatorio]

stop_words=[open('stopwords.txt', encoding='utf-8').read()]

palavras_nsw=[[palavra for palavra in palavras_ditas if not palavra in stop_words] for palavras_ditas in palavras ]

bigramas=[list(bigrams(palavra)) for palavra in palavras_nsw]