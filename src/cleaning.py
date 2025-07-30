import os
import unicodedata
import csv
import re
import sys

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


    #split sentences
    # def tokenise(text): #OP regex for cleaning punctation and splits into sentences and arrays
    #     sentences = text.lower().split('.')
    #     print(sentences)
    #     tokens = []
    #     for sentence in sentences:
    #         tokens.append(re.findall(r"\b\w+(?:['’-]\w+)*\b", sentence))
    #     print(tokens)
    #     return tokens #Returns an list of list full of tokens 
        
    #Keep sentences
def tokenise(text): #OP regex for cleaning punctation
    tokens = []
    tokens.append(re.findall(r"\b\w+(?:['’-]\w+)*\b", text.lower()))
    return tokens #Returns an list of list full of tokens

#Cleaning the massive csv i downloaded
def tsvCsv(pathToFile):
    try:
        with open(pathToFile, 'r', encoding='utf-8') as tsv:
            with open(os.path.splitext(pathToFile)[0] + ".csv", "w", encoding='utf-8', newline='') as fileOut:
                for line in tsv:
                    fileOut.write(re.sub(r"\t", ",", line))
        print("Successfully converted TSV to CSV")
    except Exception as e:
        print(f"Error: {e}")
    

def dropColumns(pathToFile, start, end):
    try:
        # Set a large but safe field size limit
        csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

        with open(pathToFile, 'r', encoding='utf-8') as fileIn:
            with open(os.path.splitext(pathToFile)[0] + "Dropped.csv", "w", encoding='utf-8', newline='') as fileOut:
                reader = csv.reader(fileIn)
                writer = csv.writer(fileOut)

                for line in reader:
                    writer.writerow(line[start:end])

        print(f"Successfully dropped columns outside range {start} to {end}")
    except Exception as e:
        print(f"Error: {e}")

def deleteRows(pathToFile, frequency):
    try:
        with open(pathToFile, 'r', encoding='utf-8') as fileIn:
            with open(os.path.splitext(pathToFile)[0] + "Shortened.csv", "w", encoding='utf-8', newline='') as fileOut:
                for i, line in enumerate(fileIn):
                    if i % frequency == 0:
                        fileOut.write(line)
    except Exception as e:
        print(e)

def test():
    #print(normaliseWord("didn't"))
    #normaliseFile("..//corpus//dictionary//english//en_GB-large.txt")
    #tsvCsv("..//corpus//text//eng_sentences_detailed.tsv")
    #dropColumns("..//corpus//text//eng_sentences_detailed.csv",2,3)
    #normaliseFile("..//corpus//text//eng_sentences_detailedDropped.csv")
    deleteRows("..//corpus//text//eng_sentences_detailedDroppedCleaned.txt",10)

if __name__ == "__main__":
    test()