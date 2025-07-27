import os
import unicodedata

#This file contains some functions that are useful for cleaning text for nlp




def normaliseWord(word): #Normalise Words to not use diacritics e.g "Asunción" -> Asuncion
    normalized = unicodedata.normalize('NFD', word)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')


def normaliseFile(pathToFile):
    try:    
        file = open(pathToFile,encoding='utf-8')
        newFile = open(os.path.splitext(pathToFile)[0] + "Cleaned.txt", "w", encoding='utf-8')
        for line in file:
            newFile.write(normaliseWord(line))
        file.close()
        newFile.close()
        return newFile.name
    except Exception as e:
        print(e)






def test():
    print(normaliseWord("didn't"))
    normaliseFile("..//corpus//dictionary//english//en_GB-large.txt")

if __name__ == "__main__":
    test()