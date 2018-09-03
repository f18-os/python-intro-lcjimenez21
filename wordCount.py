import os
import re
import sys
import collections

input = sys.argv[1]
output = sys.argv[2]

def getList():
    if os.path.exists(input):
        inputFile = open((input),"r")
        data = inputFile.read().replace('\n',' ')
        data = re.sub('\W+',' ', data)
        newData = data.split(' ')
        inputFile.close()
        print("pass")
        createDict(newData)
    else:
        print("The file %s doesn't exist" % input)

    # inputFile = open((input),"r")
    # data = readline.replace('\n',' ')
    # data = re.sub('\W+', ' ')
    # inputFile.close()


def createDict(newData):
    myDict = {}
    for word in newData:
        if word in myDict:
            myDict[word.lower()] += 1
        else:
            myDict[word.lower()] = 1

    dictionary_inOrder = collections.OrderedDict(sorted(myDict.items()))

    outputFile = open((output), "w+")
    for word in dictionary_inOrder:
        outputFile.write('%s %d\n' % (word, dictionary_inOrder[word]))
    outputFile.close()

################ Main method
getList()
