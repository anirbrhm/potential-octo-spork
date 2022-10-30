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

sentence = "Hellu what is up , would you tell me"
for word in sentence.split():
    cleaned_word = re.sub(r'[^\w\s]', '', word)  
    processed_word = cleaned_word.lower()

    print(processed_word)
