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
        for i,values in enumerate(self.transitionMatrix[word]):
            if values[1] == next:
                self.transitionMatrix[word][i][0] += 1 
                return
        self.transitionMatrix[word].append([1,next])
        



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
            f = open("..//corpus//"+file)
            self.train(f.read())
    
    def trainFromCorpusSpecific(self,filename):
        try:
            f = open("..//corpus//"+filename)
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
            word = self.randomPredict(word)
            if word == None:
                break
            text+= " " + word
        return text 

                






def test():
    M = MarkovChain()
    M.train("The Cat. didn't Sat On The Mat")
    M.trainFromCorpus()
    #print(M.getMatrix())
    print(M.predictLen("the",100))
    



if __name__ == "__main__":
    test()