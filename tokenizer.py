import re
import sys

#This function tokenizes the text file given using regular expressions
#to separate the tokens with separators that are not alphanumerical
#The complexity of this method is in linear time (O(n)) considering
#the running time increases based off the size of input
def tokenize(text):
    tokens = []
    token1ze = re.split(r"[^a-zA-Z0-9]", text)
    for x in token1ze:
        if len(x) != 0:
            tokens.append(x.lower())
    return tokens

# This function returns how many occurrences there are of a token in the text file
# It uses a dictionary to sort the token with token being the key and value being the occurrences
#The complexity of this method is also in linear time (O(n)) considering
#the running time increases based off the size of the dictionary being created
def computeWordFrequencies(token_list):
    d = {}
    for token in token_list:
        if token not in d.keys():
            d[token] = 1
        elif token in d.keys():
            d[token] += 1
    return d
#This function prints the tokens out sorted from highest occurence to lowest occurence
#The complexity of this function that prints the tokens out should be of a Constant Time Complexity
#or O(1) since we are going through a dict that is a complexity of O(1) and print also has
# a complexity of O(1)
def print_tokens(token_dict):
    if (len(token_dict.keys()) > 0):
        new_dict = sorted(token_dict.items(), key=lambda i: i[1], reverse=True)
        if (len(token_dict) < 50):
            for i in range(len(new_dict) - 1):
                            print(str(new_dict[i][0]) + "\t" + str(new_dict[i][1]))
        else:
            for i in range(50):
                print(str(new_dict[i][0]) + "\t" + str(new_dict[i][1]))

if __name__ == '__main__':
    try:
        token_list = tokenize("abc 123 dpoa asndi asdnaisd aosdnmoa asdno jq qwnen abc bc abc")
        token_dict = computeWordFrequencies(token_list)
        print_tokens(token_dict)
    except:
        print("ERROR OCCURRED FILE UNKNOWN")
        print("PLEASE TRY AGAIN")