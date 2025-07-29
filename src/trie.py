from cleaning import normaliseFile




class TrieNode:
    def __init__(self, char, endOfWord = False):
        self.char = char.lower()
        self.children = {} #Changed from arrays to dictionaries to improve memory complexity
        self.endOfWord = endOfWord

    def __repr__(self):
        return f"({self.char},{self.endOfWord})"
    
    def addChild(self,char, endOfWord = False):
        if char not in self.children:
            Node = TrieNode(char,endOfWord)
            self.children.update({char: Node})
            return Node
        if endOfWord:
            self.children[char].setEnd(endOfWord)
        return self.children[char]
    
    def getChild(self,char):
        return self.children[char]
    
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
        self.head = {}

    def __repr__(self):
        return f"{self.head}"

    def addWord(self,word): 
        #Check if node exists in head
        word = word.lower()
        char = word[0]
        if char not in self.head:
            self.head.update({char: TrieNode(char,len(word) == 1)}) #Sets end of word to true if len word is a char


        if len(word) == 1:
            return #already done added from above
        
        end = len(word) - 1
        node = self.head[char]
        for i in range(1, len(word)):
                node = node.addChild(word[i], (i == end))
            
    
    def findWord(self,word):
        if word == "":
            return True
        
        word = word.lower()
        if  word[0] in self.head:
            node = self.head[word[0]] 
        else: return False #If Root node doesnt exist

        if len(word) == 1:
            return word == node.getValue()

        i = 1
        end = len(word)
        while i < end and word[i] in node.getChildren():
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
                for childNode in node.getChildren().values():
                        stack.append((childNode, pathToNode + [childNode]))
            

        for node in self.head.values():
            dfs(node)   
        return results
    


    def fuzzySearch(self,word, maxDistance):
        #distance row
        intialRow = list(range(len(word)+1))
        results = []
        #print(prevRow)

        for node in self.head.values(): #Iterate through the head's children and runs a FuzzySearch on each one thats not None
            #print(node)
            currentRow = leveinsteinDistance(intialRow,node.getValue(), word)
            if min(currentRow) <= maxDistance: #Prunes branches if cost is higher than max allowed
                recursiveFuzzySearch(node,word,maxDistance,currentRow,node.getValue(),results)
        return results

    def addFromFile(self, filename:str):
        try:
            path = "..//corpus//dictionary//english//"+filename
            f = open(normaliseFile(path),encoding='utf-8')
            i = 0
            for word in f:    
                word = word[:-1]
                i+=1
                self.addWord(word)
            print(f"Successfully added {i} Words") 
        except Exception as e:
            print(e)



#Realised i spelt it wrong but decided to keep lol
def leveinsteinDistance(prevRow, trie_char, word): #Calculates the number of changes to change the current path to target word and then returns the minimum changes
    currentRow = [prevRow[0] + 1]
    for j in range(1, len(word) + 1):
        insertion = currentRow[j - 1] + 1
        deletion = prevRow[j] + 1
        substitution = prevRow[j - 1] + (0 if trie_char == word[j - 1] else 1)
        currentRow.append(min(insertion, deletion, substitution))
    #print(f"{trie_char} {currentRow}")
    return currentRow


def recursiveFuzzySearch(node: TrieNode, word: str, maxDistance: int, prevRow: list, prefix: str, results: list): #types provided for intellisense
    if node.isEnd() and prevRow[-1] <= maxDistance:
        results.append((prefix, prevRow[-1]))
    #
    for child in node.getChildren().values():
        #print(child)
        char = child.getValue()
        currRow = leveinsteinDistance(prevRow, char, word)
        if min(currRow) <= maxDistance: #Prunes branches if cost is higher than max allowed
            recursiveFuzzySearch(child, word, maxDistance, currRow, prefix + char, results)



 
    
            
    







def test():
    # Node = TrieNode("a",True)
    # Node.addChild("B",False)
    # print(Node.getChildren())
    # repr(Node)
    tree = Trie()

    
    #tree.addFromFile("en_GB-large.txt")

    #Test Fuzzy Search

    tree.addWord("Joe")
    print(tree)
    print(tree.findWord("joeb"))
    print(tree.displayTrie())

    #print(tree.fuzzySearch("leveinstein",1)) 






if __name__ == "__main__":
    test()