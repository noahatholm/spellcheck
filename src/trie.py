import time
from cleaning import normaliseFile

def timed(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f"{fn.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


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

def pos(char): #Helper function that returns the positon of the array any char should be placed in
    #Special Character Support
    if char == "'":
        return 26

    #Normal Characters
    return ord(char.lower()) - 97

class Trie:
    def __init__(self):
        self.head = [None] * TOTALCHARS

    def __repr__(self):
        return f"{self.head}"

    def addWord(self,word): 
        #Check if node exists in head
        char = word[0]
        if self.head[pos(char)] == None:
            self.head[pos(char)] = TrieNode(char,False)

        end = len(word) - 1
        node = self.head[pos(char)]
        for i,char in enumerate(word):
            
            node = node.addChild(char,i == end)
            #print(node) 
            
    
    def findWord(self,word):
        if word == "":
            return True
        
        node = self.head[pos(word[0])] #If Root node doesnt exist
        if node == None:
            return False


        i = 0
        end = len(word)
        while i < end and node.getChild(word[i]) != None:
            node = node.getChild(word[i])
            i+=1

        return node.isEnd() and (i == (end))
    
    @timed
    def displayTrie(self): #Performs Dfs on the trie to return a list of all the words in the trie
        results = []

        def dfs(root: TrieNode):
            stack = [(root, [])]
            while(stack):
                #print(stack)
                node,pathToNode = stack.pop()
                if node.isEnd():
                    results.append("".join(map(TrieNode.getValue,pathToNode)))
                for childNode in node.getChildren():
                    if childNode != None:
                        stack.append((childNode, pathToNode + [childNode]))
            

        for head in self.head:
            if head:
                dfs(head)   
        return results



   


        

    
            
    
def addFromFile(tree:Trie, filename:str):
    path = "..//corpus//dictionary//english//"+filename
    f = open(normaliseFile(path),encoding='utf-8')
    i = 0
    for word in f:    
        word = word[:-1]
        i+=1
        tree.addWord(word)
    print(f"Successfully added {i} Words")






def test():
    # Node = TrieNode("a",True)
    # Node.addChild("B",False)
    # print(Node.getChildren())
    # repr(Node)
    tree = Trie()
    # tree.addWord("bee")
    # tree.addWord("b")
    ##tree.addWord("Sexyback")
    tree.addWord("didn't")
    #print(tree)
    print(tree.findWord("didn't"))
    
    addFromFile(tree,"en_GB-large.txt")




if __name__ == "__main__":
    test()