import re
import csv
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
#nltk.download('all')
#nltk.download('wordnet')
#nltk.download('stopwords')

def text_preprocessing():
    #csv file -> dataset 변환
    file = open("../data/scuba_diving_safety.csv", "r", encoding="utf-8")
    rdr = csv.reader(file)
    dataset = []
    for row in rdr:
        dataset.append(row[3])
    #csv header("abstract") 0번째 요소 list에서 삭제
    dataset.pop(0)
    file.close()

    #문장 토큰화
    sent_token = []
    for i in range(len(dataset)):
        for sent in sent_tokenize(dataset[i]):
            sent_token.append(sent)

    #특수문자 제거 및 소문자로 통일
    for i in range(len(sent_token)):
        temp = re.sub(r"[^a-zA-Z]", " ", sent_token[i])
        sent_token[i] = temp.lower()

    #단어 토큰화
    word_token = []
    for i in range(len(sent_token)):
        for word in word_tokenize(sent_token[i]):
            word_token.append(word)

    #stopword 제거
    stop_words = set(stopwords.words("english"))
    word_token = [i for i in word_token if i not in stop_words]

    #어근 동일화 -> 어간 추출에서 Porter어간 추출기가 정확도가 높다고 함 // 표제어 추출도 가능한데 정확도가 더 높은 것 선택하면 될 듯
    stemmer = PorterStemmer()
    word_token = [stemmer.stem(i) for i in word_token]

    return word_token