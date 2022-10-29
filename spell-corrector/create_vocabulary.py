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

def minDistance(word1, word2):
    """Dynamic programming solution"""
    m = len(word1)
    n = len(word2)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        table[i][0] = i
    for j in range(n + 1):
        table[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
    return table[-1][-1]

print(minDistance("good","goud"))

def correctSentence(sentence) : 
    for word in line.split():
        
