
# spellcheck  
**Python Spell Check & Auto-Complete using Higher-Order Markov Chains**

This project was born from my interest in stochastic models like Markov chains. It gave me the chance to explore them while improving my skills in data structures, algorithms, and natural language processing. It also marks my first time creating a Python package installable via `pip`.


## Installation

```bash
pip install git+https://github.com/noahatholm/spellcheck
```

```python
from spellcheck.spellcheck import spellchecker

#Create an instance (language defaults to English; currently, only English is supported)
#Can also pass in a N2MarkovChain type to work with higher order markov chains
s = spellchecker()

```
## Features

I also created a simple word processor in Tkinter to better demonstrate the spellchecker than just using a CLI.

### Fast Spellchecking

- Uses a **trie data structure** for fast lookup and fuzzy matching

### Smart Suggestions

1. **Fuzzy Matching**  
   - Uses a custom Levenshtein distance algorithm to find similar words via trie traversal  
2. **Context Awareness**  
   - Predicts the most likely next words using a Markov chain based on sentence structure  
3. **Frequency Bias**  
   - Prefers more commonly used English words to improve relevance

### Self-Learning (Optional)

- The model can be updated dynamically with each word typed to improve personalisation  
- If you enable this, it’s recommended to remove the default text corpus otherwise learning process would take alot longer #Note the trie uses the text data to gather frequency data so suggestions could be less accurate until its learnt of enough text

Example of different suggestions based on the previous context

![Context Suggestions](https://i.imgur.com/bDEaBVp.gif)

Spellchecking

![Example](https://i.imgur.com/JwfQVGN.gif)


## Corpus

The system is trained on two types of text:

- **Text (Full Sentences)** – Used to build the Markov chain  
- **Dictionary Corpus (Word List)** – Used to populate the trie for spellchecking, organized by language

### Default Corpus

#### Text Corpus

- Based on 1.9 million English sentences from [Tatoeba](https://tatoeba.org/en/downloads)  
- Trimmed down to 190,000 sentences for improved performance and reduced memory usage

#### Dictionary

- Includes approximately 170,000 British English words, including names, places, and alternative spellings  
- Sourced from [this repository](https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/)  
- The dataset includes both ise and ize spellings, as both are valid in British English
