import os
import json
import nltk
import string
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

postingList = {}
path = '/home/arpn/Semester 2/Information Retrieval/Assignment 1/testdata'
stop_words = stopwords.words('english') + list(string.punctuation)


#Creating wordcloud
def createwordclouddocfreq():
    dir = path.dirname(__file__)
    words = open(path.join(dir, 'cloud.txt')).read()
    tempwords = WordCloud(collocations=False, width=10000, height=5000).generate(words)
    plt.figure()
    plt.imshow(tempwords, interpolation='bilinear')
    plt.axis("off")
    plt.show()


#tokenizing,stop-word removal and stemming
def preProcess(sentence):
    sentence = sentence.lower().decode('cp1252')
    ps = PorterStemmer()
    words = []
    tokens = nltk.word_tokenize(sentence)
    for w in tokens:
        if w in stop_words:
            tokens.remove(w)
        else:
            try:
                tempWord = ps.stem(w)
                words.append(tempWord)
            except:
                print(w)
    return words


def createwordcloud():
    f = open("cloudWordFreq.txt", "w")
    cnt = 0
    for key, value in reversed(sorted(postingList.iteritems(), key=lambda (v, k): (k, v))):
        if cnt == 500:
            break
        for _ in range(value):
            if _ == key-1:
                f.write(key+" ")
            else:
                f.write(key+".\n")
        cnt += 1


dirs = os.listdir(path)
for folder in dirs:
    files = os.listdir(path+'/'+folder)
    for id in files:
        lenDoc = 0
        fileData = [line.rstrip('\n') for line in open(path+'/'+folder+'/'+id)]
        for line in fileData:
            if line[:7] == "Lines: ":
                lenDoc = int(line[7:])
                break
        fileData = fileData[-lenDoc:]
        for line in fileData:
            words = preProcess(line)
            for w in words:
                if w in postingList.keys():
                    postingList[w] += 1
                else:
                    postingList[w] = 1

# createwordclouddocfreq()
# postingList = json.load(open('model.json'))
# f = open('cloud.txt', 'w')
# for w in postingList.keys():
#     try:
#         for _ in range(len(postingList[w])-1):
#             f.write(w+' ')
#         f.write(w + '.\n')
#     except:
#         print(w)
# f.close()
