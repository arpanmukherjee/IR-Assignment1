import re
import sys
import json
import time
import string
from math import sqrt
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

postingList = json.load(open('model.json'))
docId = [line.rstrip('\n') for line in open('docId.txt')]
stop_words = stopwords.words('english') + list(string.punctuation)


def checkWord(word):
    return re.sub(r'[^\x00-\x7F]+', '', word)


def alphanumeric(word):
    return re.sub(r'\W+', '', word)


#x OR y
def solve1(x, y):

    i = j = 0
    ans = []
    if x not in postingList.keys():
        if y not in postingList.keys():
            return ans
        else:
            return postingList[y]
    else:
        if y not in postingList.keys():
            return postingList[x]
    while i < len(postingList[x]) and j < len(postingList[y]):
        if postingList[x][i] == postingList[y][j]:
            ans.append(postingList[x][i])
            i += 1
            j += 1
        elif postingList[x][i] < postingList[y][j]:
            ans.append(postingList[x][i])
            i += 1
        else:
            ans.append(postingList[y][j])
            j += 1
    return ans


#x AND y
def solve2(x, y):
    counter = i = j = 0
    if x not in postingList.keys() or y not in postingList.keys():
        return []
    ans = []
    while i < len(postingList[x]) and j < len(postingList[y]):
        counter += 1
        if postingList[x][i] == postingList[y][j]:
            ans.append(postingList[x][i])
            i += 1
            j += 1
        elif postingList[x][i] < postingList[y][j]:
            i += 1
        else:
            j += 1
    print("No of iterations: " + str(counter))
    return ans


#x AND y with skip
def solve2Skip(x, y):
    if x not in postingList.keys() or y not in postingList.keys():
        return []
    graphXAxis = []
    graphYAxis = []
    ans = []

    skip1 = int(sqrt(len(postingList[x])))
    skip2 = int(sqrt(len(postingList[y])))
    for _ in range(6):
        # print(str(len(graphXAxis)) + ' ' + str(len(graphYAxis)))
        counter = i = j = 0
        while i < len(postingList[x]) and j < len(postingList[y]):
            if postingList[x][i] == postingList[y][j]:
                ans.append(postingList[x][i])
                i += 1
                j += 1
                counter += 1
            elif postingList[x][i] < postingList[y][j]:
                if i % skip1 == 0 and i+skip1 < len(postingList[x]) and postingList[x][i+skip1] <= postingList[y][j]:
                    while i+skip1 < len(postingList[x]) and postingList[x][i+skip1] <= postingList[y][j]:
                        i += skip1
                        counter += 1
                else:
                    i += 1
                    counter += 1
            else:
                if j % skip2 == 0 and j+skip2 < len(postingList[y]) and postingList[y][j+skip2] <= postingList[x][i]:
                    while j+skip2 < len(postingList[y]) and postingList[y][j+skip2] <= postingList[x][i]:
                        j += skip2
                        counter += 1
                else:
                    j += 1
                    counter += 1

        # print(str(len(graphXAxis)) + ' ' + str(len(graphYAxis)))
        print("For the skip size: "+str(skip2)+" No of iterations: "+str(counter))
        graphXAxis.append(int(skip2))
        graphYAxis.append(int(counter))
        # print(str(len(graphXAxis)) + ' ' + str(len(graphYAxis)))
        skip1 /= 2
        skip2 /= 2
        skip1, skip2 = int(skip1), int(skip2)
        if skip1 == 0 or skip2 == 0:
            break
    plt.plot(graphXAxis, graphYAxis)
    plt.xlabel('Skip Size')
    plt.ylabel('No of iteration')
    # plt.show()
    return ans


#x AND NOT y
def solve3(x, y):
    i = j = 0
    ans = []
    if x not in postingList.keys():
        return ans
    if y not in postingList.keys():
        return postingList[x]
    while i < len(postingList[x]) and j < len(postingList[y]):
        if postingList[x][i] == postingList[y][j]:
            i += 1
            j += 1
        elif postingList[x][i] < postingList[y][j]:
            ans.append(postingList[x][i])
            i += 1
        else:
            j += 1
    return ans


#x OR NOT y
def solve4(x, y):
    if y not in postingList.keys():
        ans = [i for i in range(19996)]
    else:
        if x not in postingList.keys():
            ans = [i for i in range(19996) if i not in postingList[y]]
        else:
            ans = [i for i in range(19996) if i not in postingList[y] or i in postingList[x]]
    return ans


def showoutput(ans):
    if len(ans) == 0:
        print("Sorry no documents found for your query!")
    else:
        print(x + " " + y)
        print("Following are the documents for your query:")
        for doc in ans:
            print docId[doc]


notY = False
x = sys.argv[1]
oper = sys.argv[2]
lm = WordNetLemmatizer()
if sys.argv[3] == 'NOT':
    notY = True
    y = sys.argv[4]
else:
    y = sys.argv[3]


if x in stop_words:
    x = ''
if y in stop_words:
    y = ''
x = lm.lemmatize(alphanumeric(checkWord(x)))
y = lm.lemmatize(alphanumeric(checkWord(y)))


if oper == 'OR':
    if notY:
        ans = solve4(x, y)
    else:
        ans = solve1(x, y)
    showoutput(ans)
elif oper == 'AND':
    if notY:
        ans = solve3(x, y)
        showoutput(ans)
    else:
        print("Using Merge postings algorithm:")
        ans = solve2(x, y)
        showoutput(ans)
        print("Using Skip pointers algorithm:")
        ans = solve2Skip(x, y)
else:
    print("Please strictly follow the input format.")
    sys.exit()
