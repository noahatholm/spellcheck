from collections import defaultdict
import random
import os
import re




class MarkovChain:
    def __init__ (self):
        self.transitionMatrix = defaultdict(list)


    def getMatrix(self):
        return self.transitionMatrix

    #Training a First Order Chain
    def addWord(self, word, next):
        self.transitionMatrix[word].append(next)
    


    def tokenize(self,text): #OP regex for cleaning punctation and splits
        return re.findall(r"\b\w+(?:['’-]\w+)*\b", text.lower())

    def train(self,text):
        tokens = self.tokenize(text)
        for i in range(len(tokens)-1):
            self.addWord(tokens[i],tokens[i+1])

    def trainFromCorpus(self):
        for file in os.listdir("..//corpus"):
            f = open("..//corpus//"+file)
            self.train(f.read())
    
    def trainFromCorpusSpecific(self,filename):
        try:
            f.open("..//corpus//"+filename)
            self.train(f.read())
        except Exception as e:
            print(f"Error {e}")


    def randomPredict(self,word):
        if not self.transitionMatrix[word]:
            return None
        return (random.choices(self.transitionMatrix[word])[0])
        

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
    #M.train("The Cat Sat On The Mat")
    M.trainFromCorpus()
    #print(M.getMatrix())
    print(M.predictLen("the",100))
    



if __name__ == "__main__":
    test()