import os
import math
import pickle

from . import markov
from . import trie
from . import cleaning



class spellchecker:
    def __init__(self,markov = markov.N1MarkovChain(),language = "english"):
        self.markovChain = markov
        self.trie = trie.Trie()
        self.lang = language

        try:
            self.loadMarkovChain()
            self.loadTrie()
            print("Successfully Loaded Trie and Markov Chain")
        except Exception as e:
            print(f"Error: Creating new Trie and Markov Chain \n{e}")
            self.__buildTrie(self.lang)
            self.buildMarkovChain()
            self.saveMarkovChain()
            self.saveTrie()

    def getMarkov(self):
        return self.markovChain
    
    def getTrie(self):
        return self.trie
    
    def getLang(self):
        return self.lang

    def __buildTrie(self,language): #Trains trie 
        try:
            if language.lower() == "en" or "english":
                file = "en_GB-larger.txt"
            self.trie.addFromFile(file)
        except Exception as e:
            print(e)

    def buildMarkovChain(self):
        self.markovChain.trainFromCorpus(self.trie) #Passing in the trie to also increment the frequency of each word
        print("Built Markov Chain off corpus")

    def checkspelling(self,word):
        return self.trie.findWord(cleaning.normaliseWord(word))
    
    def getSuggestions(self,word,suggestionsCount = 0): #checks spelling of a word and if its incorrect it will return a list of suggested spellings
        if not self.checkspelling(word):
            suggestions = []
            i = 1
            while len(suggestions) < suggestionsCount and i < 20: #20 is exit value to prevent infinite loop
                #print(suggestions)
                suggestions = (self.trie.fuzzySearch(word,i))
                i+=1
            return (sorted(suggestions,key=lambda x: x[1]))[:suggestionsCount]
        return True            

    def __normaliseSuggestions(self,levenshtein,context): #Function normalises the three factors and combines them into one order list of the best suggestions
        results = []
        maxA = max(levenshtein,key =lambda x :x[1] )[1]
        minA = min(levenshtein,key =lambda x :x[1])[1]
        maxB = max(levenshtein,key=lambda x:x[2])[2] #yeezy yeezy
        maxB = 2 if maxB == 1 else maxB
        weight = 0.7 #Weight given to factor A
        contextWeight = 1.5 #Weight Given to suggestions if they appear in the context suggestions
        commonSuggestions = set(row[0] for row in levenshtein) & set(row[1] for row in context) #Suggestions that are common to both sets

        for entry in levenshtein:
    
            word = entry[0]
            a = entry[1]
            b = entry[2]
            difA = 1 if (maxA - minA) == 0 else (maxA - minA)
        
            aNorm = 1 - ((a - minA) / (difA)) #Inverted and normalised
            bNorm = 0 if b == 0 else (math.log(b) / math.log(maxB)) #Log'd and normalised
            combined = weight * aNorm + (1 - weight) * bNorm #Combine values and multiply by weights

            if word in commonSuggestions:
                combined = min(combined * contextWeight, 1.1)

            

            results.append((word,combined))
        return sorted(results,key=lambda x:x[1],reverse = True)
        

    def smartSuggestions(self,word,suggestionsCount = 5,lastword = None): #give a tuple for lastword if using higher order markov chains
        finalSuggestions = [] #an order compilation of all the best suggestions based on 3 factors
        contextPredictions = [] 
        levenshteinSuggestions = self.getSuggestions(word,suggestionsCount)
        if levenshteinSuggestions == True: return True
        if lastword:
            contextPredictions = self.markovChain.predictTop(lastword,30)
            #print(contextPredictions)

        #print(levenshteinSuggestions)

        finalSuggestions = self.__normaliseSuggestions(levenshteinSuggestions,contextPredictions) #best suggestions comprised of levenshtein distance & word frequency
        return finalSuggestions

    def saveMarkovChain(self): #Saves markov chain to pickle file
        try:
            baseDir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(baseDir,"data","markov.pickle")    
            with open(path, 'wb') as f:
                pickle.dump(self.markovChain,f)
        except Exception as e:
            raise(e)

    def saveTrie(self):
        try:
            baseDir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(baseDir,"data","trie.pickle")   
            with open(path, 'wb') as f:
                pickle.dump(self.trie,f)
        except Exception as e:
            raise(e)

    def loadMarkovChain(self):
        try:
            baseDir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(baseDir,"data","markov.pickle")   
            with open(path, 'rb') as f:
                self.markovChain = pickle.load(f)
        except Exception as e:
            raise(e)

    def loadTrie(self):
        try:
            baseDir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(baseDir,"data","trie.pickle")   
            with open(path, 'rb') as f:
                self.trie = pickle.load(f)
        except Exception as e:
            raise(e)

    def addWord(self,word,next): #Adds word to markov tree to make it selflearning #Remember to save trie and markov regularly
        try:
            self.markovChain.addWord(word,next,self.trie)
        except Exception as e:
            raise e
    
    def addWordToDict(self,word):
        try:
            self.trie.addWord(word)
        except Exception as e:
            raise e



    

def test():
    s = spellchecker()
    #s.buildMarkovChain()
    #s.saveMarkovChain()
    #s.loadMarkovChain()
    #print(sorted(s.getTrie().displayTrie()))
    #print(s.getMarkov())
    print(s.smartSuggestions("hardon",25,"large"))


if __name__ == "__main__":
    test()
