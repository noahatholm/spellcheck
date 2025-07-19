from collections import defaultdict
import random
import os
import re




class MarkovChain:
    def __init__ (self):
        self.transitionMatrix = defaultdict(list)


    def getMatrix(self):
        return self.transitionMatrix

    #Adds a new word to the transitionMatrix and decreases the probability of the other values
    def addWord(self, word, next):
        back = 0 #back window of sliding window approach used to keep the results in order to ensure faster fetch times
        for i,values in enumerate(self.transitionMatrix[word]):
            if values[1] == next:
                self.transitionMatrix[word][i][0] += 1
                self.transitionMatrix[word][back],self.transitionMatrix[word][i] = self.transitionMatrix[word][i],self.transitionMatrix[word][back] #Swap front and back values
                return
            if self.transitionMatrix[word][i][0] < self.transitionMatrix[word][back][0]:
                back = i #Move window forward
        self.transitionMatrix[word].append([1,next]) #If not already in array add it to end with default value of 1 
        



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
    


    def train(self,text):
        tokens = self.tokenize(text)
        for sentence in tokens:    
            for i in range(len(sentence)-1):
                self.addWord(sentence[i],sentence[i+1])

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


    def randomPredict(self,word):
        if not self.transitionMatrix[word]:
            return None
        return((random.choices(self.transitionMatrix[word])))[0][1]
        
    def predictBest(self,word):
        if not self.transitionMatrix[word]:
            return None
        return max(self.transitionMatrix[word])[1]

    def predictLen(self,word,Maxlength):
        text = word
        for i in range(Maxlength):
            word = self.predictBest(word)
            if word == None:
                break
            text+= " " + word
        return text 

    def displayMatrix(self):
        for key in self.transitionMatrix:
            print(f"Key {key}: Value:{self.transitionMatrix[key]}")     


    def checkorder(self):
        for key in self.transitionMatrix:
            prev = 1000000000
            for subarray in self.transitionMatrix[key]:
                if subarray[0] > prev:
                    print("Not in order")
                    print(f"Key {key}: Value:{self.transitionMatrix[key]}")   
                prev = subarray[0]




def test():
    M = MarkovChain()
    #M.train("The Mat. didn't Sat On The Mat The Cat The Cat The Cat")
    M.trainFromCorpus()
    #M.trainFromCorpusSpecific("bingusdict.txt")
    #print(M.getMatrix())
    #M.displayMatrix()
    M.checkorder()
    #print(M.predictLen("noah",1000))
     



if __name__ == "__main__":
    test()