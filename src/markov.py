from abc import ABC, abstractmethod
from collections import defaultdict
import random
import os
import re

class MarkovChain(ABC):
    def __init__ (self):
        self.transitionMatrix = defaultdict(list)


    def getMatrix(self):
        return self.transitionMatrix
    
    #split sentences
    # def tokenize(self,text): #OP regex for cleaning punctation and splits into sentences and arrays
    #     sentences = text.lower().split('.')
    #     print(sentences)
    #     tokens = []
    #     for sentence in sentences:
    #         tokens.append(re.findall(r"\b\w+(?:['’-]\w+)*\b", sentence))
    #     print(tokens)
    #     return tokens #Returns an list of list full of tokens 
        
    #Keep sentences
    def tokenize(self,text): #OP regex for cleaning punctation
        tokens = []
        tokens.append(re.findall(r"\b\w+(?:['’-]\w+)*\b", text.lower()))
        return tokens #Returns an list of list full of tokens

    def trainFromCorpus(self):
        for file in os.listdir("..//corpus"):
            f = open("..//corpus//"+file,encoding='utf-8')
            self.train(f.read())
    
    def trainFromCorpusSpecific(self,filename):
        try:
            f = open("..//corpus//"+filename,encoding='utf-8')
            self.train(f.read())
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

 
    @abstractmethod
    def randomPredict(self,word,topN):
        pass

    @abstractmethod
    def train(self,text):
        pass     

    
    @abstractmethod
    def predict(self,word,topN): #topN 0 to randomly choose from all, topN = 1 to always choose mostlikely, topN > 1: specify how many are in the pool to randomly choose
        pass





class N1MarkovChain(MarkovChain):
    #Adds a new word to the transitionMatrix and decreases the probability of the other values
    def addWord(self, word, next):
        back = 0 #back window of sliding window approach used to keep the results in order to ensure faster fetch times
        for i,values in enumerate(self.transitionMatrix[word]):
            if self.transitionMatrix[word][i][0] < self.transitionMatrix[word][back][0]:
                back = i #Move window forward
            if values[1] == next:
                self.transitionMatrix[word][i][0] += 1
                self.transitionMatrix[word][back],self.transitionMatrix[word][i] = self.transitionMatrix[word][i],self.transitionMatrix[word][back] #Swap front and back values
                return
            
        self.transitionMatrix[word].append([1,next]) #If not already in array add it to end with default value of 1 
        

    def train(self,text):
        tokens = self.tokenize(text)
        for sentence in tokens:    
            for i in range(len(sentence)-1):
                self.addWord(sentence[i],sentence[i+1])


    def randomPredict(self, word, topN):
        if topN == 0:
            return (random.choice(self.transitionMatrix[word])[1])
        else:
            return (random.choice(self.transitionMatrix[word][0:topN])[1])
    


    def predict(self,word,topN):
        if not self.transitionMatrix[word.lower()]:
            return None
        if topN == 1:
            return self.transitionMatrix[word.lower()][0][1] #transitionMatrix is kept in order so the first item is the highest probability
        return self.randomPredict(word.lower(),0)




  







def test():
    M = N1MarkovChain()
    M.train("the cat sat on the mat ")
    #M.trainFromCorpus()
    #M.trainFromCorpusSpecific("bingusdict.txt")
    #print(M.getMatrix())
    M.displayMatrix()
    M.checkorder()
    print(M.predictLen("The",1000,2))
     



if __name__ == "__main__":
    test()