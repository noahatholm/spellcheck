from abc import ABC, abstractmethod
from collections import defaultdict
import random
import os
import importlib.resources as package

import trie
from cleaning import tokenise

class MarkovChain(ABC):
    def __init__ (self):
        self.transitionMatrix = defaultdict(list)

    def __repr__(self):
        matrix = ""
        for key in self.transitionMatrix:
            matrix += (f"Key {key}: Value:{self.transitionMatrix[key]}\n")
        return matrix

    def getMatrix(self):
        return self.transitionMatrix
    


    def trainFromCorpus(self, frequencyTrie: trie.Trie = None): 
        try:
            baseDir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(baseDir,"corpus","text")
            for file in os.listdir(path):
                with open(os.path.join(path,file), encoding='utf-8') as f:
                    self.train(f.read(), frequencyTrie)
        except Exception as e:
            print(e)
    
    def trainFromCorpusSpecific(self,filename, frequencyTrie: trie.Trie = None):
        try:
            baseDir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(baseDir,"corpus","text")
            with open(os.path.join(path,filename), encoding='utf-8') as f:
                self.train(f.read(), frequencyTrie)
        except Exception as e:
            print(f"Error {e}") 

    def displayMatrix(self):
        for key in self.transitionMatrix:
            print(f"Key {key}: Value:{self.transitionMatrix[key]}")  

    def checkorder(self): #Method for debugging
        for key in self.transitionMatrix:
            prev = 1000000000
            for subarray in self.transitionMatrix[key]:
                if subarray[0] > prev:
                    print("Not in order")
                    print(f"Key {key}: Value:{self.transitionMatrix[key]}")   
                prev = subarray[0] 

    def predictLen(self,word,Maxlength,topN): #topN = 0 to randomly choose from all, topN = 1 to always choose mostlikely, topN > 1: specify how many are in the pool to randomly choose 
        text = word
        for i in range(Maxlength):
            word = self.predict(word,topN)
            if word == None:
                break
            text+= " " + word
        return text

    #Adds a new word to the transitionMatrix and decreases the probability of the other values
    #Can also accept multiple words for parameter word for higher order markov chains
    def addWord(self, word, next, frequencyTrie: trie.Trie = None): #optional pass in a Trie which will then attemp to increment the frequency of the words in the trie if possible
        back = 0 #back window of sliding window approach used to keep the results in order to ensure faster fetch times
        if frequencyTrie:
                frequencyTrie.findAndIncrement(next)
        for i,values in enumerate(self.transitionMatrix[word]): 
            if self.transitionMatrix[word][i][0] < self.transitionMatrix[word][back][0]:
                back = i #Move window forward
            if values[1] == next:
                self.transitionMatrix[word][i][0] += 1
                self.transitionMatrix[word][back],self.transitionMatrix[word][i] = self.transitionMatrix[word][i],self.transitionMatrix[word][back] #Swap front and back values
                return
            
        self.transitionMatrix[word].append([1,next]) #If not already in array add it to end with default value of 1 



    @abstractmethod
    def randomPredict(self,word,topN):
        pass

    @abstractmethod
    def train(self,text, frequencyTrie: trie.Trie = None): #optional pass in a Trie which will then attemp to increment the frequency of the words in the trie if possible
        pass     

    
    @abstractmethod
    def predict(self,*args, **kwargs): #topN 0 to randomly choose from all, topN = 1 to always choose mostlikely, topN > 1: specify how many are in the pool to randomly choose
        pass


    @abstractmethod
    def predictLen(self,*args, **kwargs):
        pass


    @abstractmethod
    def predictTop(self,*args, **kwargs):
        pass




class N1MarkovChain(MarkovChain):
    def train(self,text, frequencyTrie: trie.Trie = None):
        tokens = tokenise(text)
        for sentence in tokens:    
            for i in range(len(sentence)-1):
                self.addWord(sentence[i],sentence[i+1],frequencyTrie)


    def randomPredict(self, word, topN):
        if topN == 0:
            return (random.choice(self.transitionMatrix[word])[1])
        else:
            return (random.choice(self.transitionMatrix[word][0:topN])[1])
    


    def predict(self,word,topN = 1):
        if not self.transitionMatrix[word.lower()]:
            return None
        if topN == 1:
            return self.transitionMatrix[word.lower()][0][1] #transitionMatrix is kept in order so the first item is the highest probability
        return self.randomPredict(word.lower(),0)
    
    def predictLen(self,word,Maxlength,topN): #topN = 0 to randomly choose from all, topN = 1 to always choose mostlikely, topN > 1: specify how many are in the pool to randomly choose 
        text = word
        for i in range(Maxlength):
            word = self.predict(word,topN)
            if word == None:
                break
            text+= " " + word
        return text

    def predictTop(self, word, amount):
        array = self.transitionMatrix[word.lower()]
        if len(array) < amount:
            return array
        else:
            return array[0:amount]

class N2MarkovChain(MarkovChain): #Appends words to the dictionary as a tuple of (word1,word2): word3
    def train(self,text, frequencyTrie: trie.Trie = None):
        tokens = tokenise(text)
        for sentence in tokens:
            for i in range(len(sentence)-2):
                self.addWord((sentence[i],sentence[i+1]),sentence[i+2],frequencyTrie)


    def randomPredict(self, lastlastword,lastword, topN):
        if topN == 0:
            return (random.choice(self.transitionMatrix[(lastlastword,lastword)])[1])
        else:
            return (random.choice(self.transitionMatrix[(lastlastword,lastword)][0:topN])[1])
    


    def predict(self,lastlastword,lastword,topN = 1):
        if not self.transitionMatrix[(lastlastword.lower(),lastword.lower())]:
            return None
        if topN == 1:
            return self.transitionMatrix[(lastlastword.lower(),lastword.lower())][0][1] #transitionMatrix is kept in order so the first item is the highest probability
        return self.randomPredict(lastlastword.lower(),lastword.lower(),0)

    
    def predictLen(self,word1,word2,Maxlength,topN): #topN = 0 to randomly choose from all, topN = 1 to always choose mostlikely, topN > 1: specify how many are in the pool to randomly choose 
        text = word1 + " " + word2.lower()
        for i in range(Maxlength):
            temp = word2
            word2 = self.predict(word1,word2,topN)
            word1 = temp
            if word2 == None:
                break
            text+= " " + word2
        return text

    def predictTop(self, word1,word2, amount):
        array = self.transitionMatrix[(word1.lower(),word2.lower())]
        if len(array) < amount:
            return array
        else:
            return array[0:amount]

    








def test():
    M = N1MarkovChain()
    M.train("the cat sat on the mat ")
    M.trainFromCorpus()
    #M.trainFromCorpusSpecific("bingusdict.txt")
    #print(M.getMatrix())
    #M.displayMatrix()
    #M.checkorder()
    print(M.predictLen("The",1000,2))

     


if __name__ == "__main__":
    test()