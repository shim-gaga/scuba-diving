"""
빈도수 분석 및 Text Rank 분석으로 선정된 top 30개의 키워드를 벡터로 변환한 후, 이 키워드들에 대한 벡터를 t-SNE 그래프로 표현하여 'figure' 폴더에 저장합니다. 
   
Args:
    -d: data(document) path (required)
    -s: path to save t-SNE graph (required)
    -t: title of figure 
    -tx: path of textrank csv file (required)
    -fq: path of frequency analysis csv file (required)

Returns: 
    Saved Path: ./figure/topic name/
    Name of graph: '/topic' + save_path[-1] + '_keyword_t-SNE.png'

    t-SNE graph that expresses top 30 keywords selected by frequency analysis and TextRank into vectors. 
    Can understand the relationship between words using this graph.

입력 예시:
    python keyword_t-SNE.py -d './data/topic2/trust_robot.csv' -s '/topic2' -tx './data/topic2/topic2_Textrank.csv' -fq './data/topic2/topic2_frequency.csv'
"""

import sys
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.corpora.dictionary import Dictionary
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import seaborn as sns

sys.path.insert(0, '../')
import preprocess_csv as preprocess


def tokenizer(text):
    '''
    apply tokenizer
    '''
    cachedStopWords = stopwords.words("english")
    RegTok = RegexpTokenizer("[\w']{3,}")
    english_stops = set(stopwords.words('english'))
    tokens = RegTok.tokenize(text.lower())
    # stopwords 제외
    words = [word for word in tokens if (word not in english_stops) and len(word) > 2]
    
    stemmer = PorterStemmer()
    word_token = [stemmer.stem(i) for i in words]
    
    return word_token


def get_word_index(path, model):
    stemmer = PorterStemmer()

    df = pd.read_csv(path)
    words = df['keyword']
    index = []
    for word in words:
        index.append(model.wv.index2word.index(stemmer.stem(word)))

    return words, index


def draw_tsne(fig, x, y, color, alpha):
    # 한글 깨짐
    plt.figure(figsize=(10, 6))
    plt.rcParams['axes.unicode_minus'] = False
    # if you use MacOS
    plt.rcParams['font.family'] = 'AppleGothic'
    # else if you use Windows
    # plt.rcParams['font.family'] = 'Malgun Gothic'

    fig = sns.scatterplot(
        x=x, y=y,
        legend="full",
        color=color,
        alpha=alpha
    )
    
    if title is not None:
        fig.set(title=title)
    
    return fig.get_figure()



def main():
    filename = '/topic' + save_path[-1] + '_keyword_t-SNE.png'
    df = pd.read_csv(data_path)
    papers = preprocess.extract_text(df)
    texts = [tokenizer(paper) for paper in papers]

    # size: 임베딩된 벡터 차원
    # window: context window 크기
    # min_count: 단어 최소 빈도수
    # workers: 학습을 위한 프로세스 수
    # sg: 0은 CBOW, 1은 Skip-Gram
    model = Word2Vec(sentences=texts, size=100, window=5, min_count=2, workers=-1, sg=1)

    # load tsne model
    tsne_model = TSNE(perplexity=40, n_components=2, n_iter=2500, random_state=7)

    full_tsne_2 = tsne_model.fit_transform(model.wv.vectors)
    full_x = full_tsne_2[:, 0]
    full_y = full_tsne_2[:, 1]
    

    # save textrank tsne values
    tr_words, tr_index = get_word_index(tr_path, model)

    # save frequency tsne values
    fq_words, fq_index = get_word_index(fq_path, model)

    # find common indexes
    common = []
    for i in tr_index:
        if i in fq_index:
            common.append(i)

    common_x = []; common_y = []; common_words_ = []
    for i in common:
        common_x.append(full_tsne_2[i, 0])
        common_y.append(full_tsne_2[i, 1])

    tr_x = []; tr_y = []; tr_words_ = []
    for i in tr_index:
        if not(i in common):
            tr_x.append(full_tsne_2[i, 0])
            tr_y.append(full_tsne_2[i, 1])

    fq_x = []; fq_y = []; fq_words_ = []
    for i in fq_index:
        if not(i in common):
            fq_x.append(full_tsne_2[i, 0])
            fq_y.append(full_tsne_2[i, 1])
            
    ## draw figures
    fig = plt.figure(figsize=(10, 6))

    # drwaw tnse to full vectors
    sns.scatterplot(
        x=full_x, y=full_y,
        legend="full",
        color='gray',
        alpha=0.1
    )
    fig.set_label("All Keywords")

    # draw common index 
    fig = sns.scatterplot(
        x=common_x, y=common_y,
        legend="full",
        color='g',
        alpha=1
    )
    fig.set_label("Common Keywords")

    # draw tsne to textrank words
    fig = sns.scatterplot(
        x=tr_x, y=tr_y,
        legend="full",
        color='b',
        marker='+',
        alpha=1
    )
    fig.set_label("Keywords of TextRank")

    # draw tsne to frequency words
    sns.scatterplot(
        x=fq_x, y=fq_y,
        legend="full",
        color='r',
        marker='+',
        alpha=1
    )
    fig.set_label("Keywords of Word Frequency Counter")

    # add textrank words
    for i in range(len(common)):
        fig.text(common_x[i]+1, common_y[i]+1, tr_words[i], alpha=1, fontsize='x-small', horizontalalignment='center')

    for i in range(len(tr_x)):
        fig.text(tr_x[i]+1, tr_y[i]+1, tr_words[i], alpha=1, fontsize='x-small', horizontalalignment='center')
    
    # add frequency words
    for i in range(len(fq_x)):
        fig.text(fq_x[i]+1, fq_y[i]+1, fq_words[i], alpha=1, fontsize='x-small', horizontalalignment='center')

    fig.legend(labels=['All Keywords', 'Common keywords', 'TextRank', 'Word Frequency Counter'], loc='upper right')

    # plt.show()
    fig = fig.get_figure()
    fig.savefig('./figure' + save_path + filename)


if __name__ == '__main__':
    global data_path, save_path, title, tr_path, fq_path

    parser = argparse.ArgumentParser(description="-d input data path(csv) -s save path to store output -t title of figure -tx textrank csv path -fq frequency csv path")
    parser.add_argument('-d', help="input_data_path", required=True)
    parser.add_argument('-s', help="save_path", required=True)
    parser.add_argument('-t', help="fig_title")
    parser.add_argument('-tx', help="textrank_path", required=True)
    parser.add_argument('-fq', help="frequency_path", required=True)
    
    args = parser.parse_args()

    data_path = args.d; save_path = args.s; title = args.t; tr_path = args.tx; fq_path = args.fq
    print("data_path:", data_path)
    print("save_path:", save_path) 
    print("title of figure:", title)
    print("tr_path:", tr_path)
    print("fq_path:", fq_path)
    print()

    main()