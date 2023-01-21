import re

with open('spell-corrector/training-data.txt','r', encoding="utf8") as file:
    flag = 0  
    vocab = [] 
    for line in file:     
        for word in line.split():   
            updated_word = re.sub(r'[^\w\s]', '', word)       
            vocab.append(updated_word.lower()) 
        flag = flag + 1   

dictionary = set(vocab) 
dict_list = list(dictionary)

dict_list.remove("")

INSERTION_COST = 1.0
DELETION_COST = 1.0
SUBSTITUTION_COST = 1.0

keyboardArray = [
    ['`','1','2','3','4','5','6','7','8','9','0','-','='],
    ['q','w','e','r','t','y','u','i','o','p','[',']','\\'],
    ['a','s','d','f','g','h','j','k','l',';','\''],
    ['z','x','c','v','b','n','m',',','.','/'],
    ['', '', ' ', ' ', ' ', ' ', ' ', '', '']
    ]

# Finds a 2-tuple representing c's position on the given keyboard array.  If
# the character is not in the given array, then give appropriate penalty
def getCharacterCoord(c, array):
    row = -1
    column = -1
    for r in array:
        if c in r:
            row = array.index(r)
            column = r.index(c)
            return (row, column)
        else : 
            return (10,10) #TODO Check the penalty we want to apply 

# Finds the Euclidean distance between two characters, regardless of whether
# they're shifted or not.
def euclideanKeyboardDistance(c1, c2):
    coord1 = getCharacterCoord(c1, keyboardArray)
    coord2 = getCharacterCoord(c2, keyboardArray)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**(0.5)

# The cost of inserting c at position i in string s
def insertionCost(s, i, c):
    if not s or i >= len(s):
        return INSERTION_COST
    cost = INSERTION_COST
    cost += euclideanKeyboardDistance(s[i], c)
    return cost

# The cost of omitting the character at position i in string s
def deletionCost(s, i):
    return DELETION_COST

# The cost of substituting c at position i in string s
def substitutionCost(s, i, c):
    cost = SUBSTITUTION_COST
    if len(s) == 0 or i >= len(s):
        return INSERTION_COST

    cost += euclideanKeyboardDistance(s[i], c)
    return cost

# Finds the typo distance (a floating point number) between two strings, based
# on the canonical Levenshtein distance algorithm.
def typoDistance(s, t):

    # A multidimensional array of 0s with len(s) rows and len(t) columns.
    d = [[0]*(len(t) + 1) for i in range(len(s) + 1)]

    for i in range(len(s) + 1):
        d[i][0] = sum([deletionCost(s, j - 1) for j in range(i)])
    for i in range(len(t) + 1):
        intermediateString = ""
        cost = 0.0
        for j in range(i):
            cost += insertionCost(intermediateString, j - 1, t[j - 1])
            intermediateString = intermediateString + t[j - 1]
        d[0][i] = cost

    for j in range(1, len(t) + 1):
        for i in range(1, len(s) + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                delCost = deletionCost(s, i - 1)
                insertCost = insertionCost(s, i, t[j - 1])
                subCost = substitutionCost(s, i - 1, t[j - 1])
                d[i][j] = min(d[i - 1][j] + delCost,
                              d[i][j - 1] + insertCost,
                              d[i - 1][j - 1] + subCost)

    return d[len(s)][len(t)]

demo_vocab = ["hello", "why", "sure", "tell"]

def correctSentence(sentence) : 
    corrected_sentence = []
    for word in sentence.split():
        cleaned_word = re.sub(r'[^\w\s]', '', word)  
        processed_word = cleaned_word.lower()  

        if processed_word == '' : 
            continue     
        
        if processed_word in dict_list : 
            corrected_sentence.append(processed_word)
            continue 
        
        distance = 5.0
        correct_word = processed_word 
        for possible_correct_word in dict_list : 
            if typoDistance(processed_word, possible_correct_word) < distance :
                correct_word = possible_correct_word
                distance = typoDistance(processed_word, possible_correct_word) 
            
        corrected_sentence.append(correct_word) 

        # update the code to prefer the corrected word to start with the same letter

    return corrected_sentence

print(correctSentence("Hellu what is up , would you rell me"))