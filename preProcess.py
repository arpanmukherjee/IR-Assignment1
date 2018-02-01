import os
import re
import json
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

docIdList = []
postingList = {}
stop_words = stopwords.words('english') + list(string.punctuation)
path = '/home/arpn/Semester 2/Information Retrieval/Assignment 1/testdata'


def checkWord(word):
    return re.sub(r'[^\x00-\x7F]+', '', word)


def alphanumeric(word):
    return re.sub(r'\W+', '', word)


#tokenizing,stop-word removal and stemming
def preProcess(sentence):
    sentence = sentence.lower().decode('cp1252')
    tokens = nltk.word_tokenize(sentence)
    for w in tokens:
        if w in stop_words:
            tokens.remove(w)
        else:
            tempword = checkWord(w)
            tokens.remove(w)
            if len(tempword) != 0:
                tempword = alphanumeric(tempword)
                if len(tempword) != 0:
                    tokens.append(tempword)
    words = []
    lm = WordNetLemmatizer()
    for w in tokens:
        try:
            words.append(lm.lemmatize(w))
        except:
            print w

    return words



dirs = os.listdir(path)
docId = 0
for folder in dirs:
    # print folder
    files = os.listdir(path+'/'+folder)
    for id in files:
        docIdList.append(folder+'/'+id)
        lenDoc = 0
        fileData = [line.rstrip('\n') for line in open(path+'/'+folder+'/'+id)]
        print (folder+'/'+id)
        for line in fileData:
            if line[:7] == "Lines: ":
                lenDoc = int(line[7:])
                break
        fileData = fileData[-lenDoc:]
        for line in fileData:
            words = preProcess(line)
            for w in words:
                if w in postingList.keys():
                    postingList[w].append(docId)
                else:
                    tempList = []
                    tempList.append(docId)
                    postingList[w] = tempList
        docId += 1

for key in postingList:
    temp = set(postingList[key])
    postingList[key] = [i for i in temp]
    postingList[key].sort()


with open('model.json', 'w') as fp:
    json.dump(postingList, fp)


f = open('docId.txt', 'w')
for doc in docIdList:
    f.write(str(doc)+"\n")
f.close()
