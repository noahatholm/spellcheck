import time
from cleaning import normaliseFile
import sys



class TrieNode:
    def __init__(self, char, endOfWord = False):
        self.char = char.lower()
        self.children = [None] * TOTALCHARS
        self.endOfWord = endOfWord

    def __repr__(self):
        return f"({self.char},{self.endOfWord})"
    
    def addChild(self,char, endOfWord = False):
        if self.children[pos(char)] == None:
            Node = TrieNode(char,endOfWord)
            self.children[pos(char)] = Node
            return Node
        if endOfWord:
            self.children[pos(char)].setEnd(endOfWord)
        return self.children[pos(char)]
    
    def getChild(self,char):
        return self.children[pos(char)]
    
    def getChildren(self):
        return self.children
    
    def getValue(self):
        return self.char
    
    def isEnd(self):
        return self.endOfWord
    
    def setEnd(self,end):
        self.endOfWord = end
        
    
TOTALCHARS = 27


class Trie:
    def __init__(self):
        self.head = [None] * TOTALCHARS

    def __repr__(self):
        return f"{self.head}"

    def addWord(self,word): 
        #Check if node exists in head
        char = word[0]
        if self.head[pos(char)] == None:
            self.head[pos(char)] = TrieNode(char,len(word) == 1) #Sets end of word to true if len word is a char


        if len(word) == 1:
            return #already done added from above
        
        end = len(word) - 1
        node = self.head[pos(char)]
        for i in range(1, len(word)):
                node = node.addChild(word[i], (i == end))
            
    
    def findWord(self,word):
        if word == "":
            return True
        
        word = word.lower()

        node = self.head[pos(word[0])] #If Root node doesnt exist
        if node == None:
            return False

        if len(word) == 1:
            return word == node.getValue()

        i = 1
        end = len(word)
        while i < end and node.getChild(word[i]) != None:
            node = node.getChild(word[i])
            i+=1

        return node.isEnd() and (i == (end))
    

    def displayTrie(self): #Performs Dfs on the trie to return a list of all the words in the trie
        results = []

        def dfs(root: TrieNode):
            stack = [(root, [])]
            while(stack):
                #print(stack)
                node,pathToNode = stack.pop()
                if node.isEnd():
                    results.append(root.getValue() + "".join(map(TrieNode.getValue,pathToNode)))
                for childNode in node.getChildren():
                    if childNode != None:
                        stack.append((childNode, pathToNode + [childNode]))
            

        for head in self.head:
            if head:
                dfs(head)   
        return results
    


    def fuzzySearch(self,word, maxDistance):
        #distance row
        intialRow = list(range(len(word)+1))
        results = []
        #print(prevRow)

        for node in self.head: #Iterate through the head's children and runs a FuzzySearch on each one thats not None
            if node: #check if node is not none
                currentRow = leveinsteinDistance(intialRow,node.getValue(), word)
                if min(currentRow) <= maxDistance:
                    recursiveFuzzySearch(node,word,maxDistance,currentRow,node.getValue(),results)
        return results

    def addFromFile(self, filename:str):
        path = "..//corpus//dictionary//english//"+filename
        f = open(normaliseFile(path),encoding='utf-8')
        i = 0
        for word in f:    
            word = word[:-1]
            i+=1
            self.addWord(word)
        print(f"Successfully added {i} Words") 


def pos(char): #Helper function that returns the positon of the array any char should be placed in
    #Special Character Support
    if char == "'":
        return 26

    #Normal Characters
    return ord(char.lower()) - 97

def leveinsteinDistance(prevRow, trie_char, word): #Calculates the number of changes to change the current path to target word and then returns the minimum changes
    currentRow = [prevRow[0] + 1]
    for j in range(1, len(word) + 1):
        insertion = currentRow[j - 1] + 1
        deletion = prevRow[j] + 1
        substitution = prevRow[j - 1] + (0 if trie_char == word[j - 1] else 1)
        currentRow.append(min(insertion, deletion, substitution))
    return currentRow


def recursiveFuzzySearch(node: TrieNode, word: str, maxDistance: int, prevRow: list, prefix: str, results: list): #types provided for intellisense
    if node.isEnd() and prevRow[-1] <= maxDistance:
        results.append((prefix, prevRow[-1]))
    #
    for child in node.getChildren():
        if child:
            char = child.getValue()
            currRow = leveinsteinDistance(prevRow, char, word)
            if min(currRow) <= maxDistance:
                recursiveFuzzySearch(child, word, maxDistance, currRow, prefix + char, results)



 
    
            
    







def test():
    # Node = TrieNode("a",True)
    # Node.addChild("B",False)
    # print(Node.getChildren())
    # repr(Node)
    tree = Trie()

    
    tree.addFromFile("en_GB-large.txt")

    #Test Fuzzy Search
    # tree.addWord("cab")
    # tree.addWord("cat")
    # tree.addWord("cart")
    # tree.addWord("cut")
    # tree.addWord("dog")
    #tree.addWord("c")
    print(tree.findWord("noah"))
    #print(tree.findWord("zippier"))

    #print(tree.displayTrie())

    print(tree.fuzzySearch("noha",1))



if __name__ == "__main__":
    test()