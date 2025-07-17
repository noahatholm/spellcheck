
import numpy as np



class MarkovChain:
    def __init__ (self):
        self.transitionMatrix = [[]]


    def getMatrix(self):
        return self.transitionMatrix

    #Training a First Order Chain
    def addWord(self, word, last):
        if word not in self.transitionMatrix:
            print("nah")

    





def test():
    M = MarkovChain()
    M.addWord("yo","hi")
    print(M.getMatrix())
    



if __name__ == "__main__":
    test()