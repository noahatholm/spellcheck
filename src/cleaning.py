import re
#Simple set of functions used to clean up the next before processingk

def cleanPunctuation(text): #deletes most punctation except internal ones
    print(re.findall(r"\b\w+(?:['’-]\w+)*\b", text))

def cleanText(text):
    text = text.lower()
    text = cleanPunctuation(text)

    return text


if __name__ == "__main__":
    print(cleanText("HELLO! I doN't like u you an opp\n --     hi you smell lets co-operate"))