import markov
import trie
import cleaning
import os


class spellcheck:
    def __init__(self,markov = markov.N1MarkovChain(),language = "english"):
        self.markovChain = markov
        self.trie = trie.Trie()
        self.lang = language

        self.__buildTrie(self.lang)


    def __buildTrie(self,language): #Trains trie 
        try:
            if language.lower() == "en" or "english":
                file = "en_GB-large.txt"
            self.trie.addFromFile(file)
        except Exception as e:
            print(e)

    def buildMarkovChain(self):
        self.markovChain.trainFromCorpus()

    def checkspelling(self,word):
        return self.trie.findWord(cleaning.normaliseWord(word))
    
    def processWord(self,word,suggestionsCount = 0): #checks spelling of a word and if its incorrect it will return a list of suggested spellings
        if not self.checkspelling(word):
            suggestions = []
            i = 1
            while len(suggestions) < suggestionsCount:
                suggestions = (self.trie.fuzzySearch(word,i))
                print(f"{len(suggestions)} {suggestionsCount}")
                i+=1
            return suggestions[:suggestionsCount]
        return True            
            


    

def test():
    s = spellcheck()
    print(s.processWord("catr",5))

if __name__ == "__main__":
    test()