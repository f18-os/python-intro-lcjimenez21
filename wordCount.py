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
        if '-' in data: #break words with '-'
            data.replace('-', ' ')
        data = re.sub('\W+',' ', data)
        data = re.sub('\s+', ' ', data)
        newData = data.split(' ')
        inputFile.close()
        print("Pass") #debug tool
        createDict(newData)
    else:
        print("The file %s doesn't exist" % input)


def createDict(newData):
    myDict = {}
    #add words to dictionary
    for word in newData:
        #if word exist repetition has occur keep count of repetions
        if word.lower() in myDict:
            myDict[word.lower()] += 1
            pass

        #if a nothing(blank space) occurs just ignore, add instance of word
        elif not word == '':
            myDict[word.lower()] = 1
            pass

    #make dictionary in alphabetical order
    dictionary_inOrder = collections.OrderedDict(sorted(myDict.items()))

    '''create my output file with all words along the number of times it appear
    on the input file'''
    outputFile = open((output), "w+")
    for word in dictionary_inOrder:
        outputFile.write('%s %d\n' % (word, dictionary_inOrder[word]))

    outputFile.close()

################ Main method ######################
getList()
