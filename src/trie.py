class TrieNode:
    def __init__(self, char, endOfWord = False):
        self.char = char.lower()
        self.children = [None] * 26
        self.endOfWord = endOfWord

    def __repr__(self):
        return f"({self.char},{self.endOfWord})"
    
    def addChild(self,char, endOfWord = False):
        if self.children[pos(char)] == None:
            Node = TrieNode(char,endOfWord)
            self.children[pos(char)] = Node
            return Node
        return self.children[pos(char)]
    
    def getChild(self,char):
        return self.children[pos(char)]
    
    def getChildren(self):
        return self.children
    
    def getValue(self):
        return self.char
    
    def isEnd(self):
        return self.endOfWord
    


def pos(char): #Helper function that returns the positon of the array any char should be placed in
    return ord(char.lower()) - 97

class Trie:
    def __init__(self):
        self.head = [None] * 26

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
   


        

    
            
    





def test():
    # Node = TrieNode("a",True)
    # Node.addChild("B",False)
    # print(Node.getChildren())
    # repr(Node)
    tree = Trie()
    tree.addWord("sexy")
    #print(tree)
    print(tree.findWord("sexyb"))



if __name__ == "__main__":
    test()