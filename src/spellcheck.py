import markov
import trie
import cleaning
import math
import pickle

class spellcheck:
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
                file = "en_GB-large.txt"
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

    def __normaliseSuggestions(self,levenshtein): #Function normalises the two factors and combines them into one order list of the best suggestions
        results = []
        maxA = max(levenshtein,key =lambda x :x[1] )[1]
        minA = min(levenshtein,key =lambda x :x[1])[1]
        maxB = max(levenshtein,key=lambda x:x[2])[2] #yeezy yeezy
        weight = 0.7 #Weight given to factor A
        for entry in levenshtein:
    
            word = entry[0]
            a = entry[1]
            b = entry[2]
            aNorm = 1 - ((a - minA) / (maxA - minA)) #Inverted and normalised
            bNorm = 0 if b == 0 else (math.log(b) / math.log(maxB)) #Log'd and normalised
            combined = weight * aNorm + (1 - weight) * bNorm #Combine values and multiply by weights
            results.append((word,combined))
        return sorted(results,key=lambda x:x[1],reverse = True)
        

    def smartSuggestions(self,word,suggestionsCount = 5):
        finalSuggestions = [] #an order compilation of all the best suggestions based on 3 factors 
        levenshteinSuggestions = self.getSuggestions(word,50)
        if levenshteinSuggestions == True: return True
        contextPredictions = self.markovChain.predictTop(word,20)
        #print(levenshteinSuggestions)

        normal = self.__normaliseSuggestions(levenshteinSuggestions) #best suggestions comprised of levenshtein distance & word frequency
        return normal

    def saveMarkovChain(self): #Saves markov chain to pickle file
        try:
            with open('..//data//markov.pickle', 'wb') as f:
                pickle.dump(self.markovChain,f)
        except Exception as e:
            raise(e)

    def saveTrie(self):
        try:
            with open('..//data//trie.pickle', 'wb') as f:
                pickle.dump(self.trie,f)
        except Exception as e:
            raise(e)

    def loadMarkovChain(self):
        try:
            with open('..//data//markov.pickle', 'rb') as f:
                self.markovChain = pickle.load(f)
        except Exception as e:
            raise(e)

    def loadTrie(self):
        try:
            with open('..//data//trie.pickle', 'rb') as f:
                self.trie = pickle.load(f)
        except Exception as e:
            raise(e)

    

def test():
    s = spellcheck()
    #s.buildMarkovChain()
    #s.saveMarkovChain()
    #s.loadMarkovChain()
    #print(sorted(s.getTrie().displayTrie()))
    #print(s.getMarkov())
    print(s.smartSuggestions("levenstinn",25))


if __name__ == "__main__":
    test()