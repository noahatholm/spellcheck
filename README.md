# spellcheck
Python Spell Check &amp; Auto Complete using higher order markov chains



## Corpus
Theres two types of corpus that the project is trained on.
* Text (Full Sentences) used for markov chains
* Dictionary (List of Words) used for populating the trie used in spellcheck seperated by Languages

### Defualt Corpus
#### Text
Some basic texts I used to develop, not very extensive

#### Dictionary
included 170k British English Words
These are the majority of English words + Names, Places etc
Taken from this [repository](https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/)
I've chosen the large dataset which is comprised of both ise and ize spellings of english words because in British English both are techncially correct

