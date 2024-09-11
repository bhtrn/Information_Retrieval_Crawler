import os 
import json
from bs4 import BeautifulSoup 
from nltk.stem import PorterStemmer
import tokenizer

DocIDtoURL = dict() # {docID: url}
Allunique = set()
Term_index = dict()
def indexer():
    global Term_index
    global DocIDtoURL
    global Allunique
    files_count = 0
    stored_indices = 0

    for folder in os.listdir('DEV'):
        if folder == '.DS_Store':       
            continue
        indexes = dict() # {token: {docID: [freq, importantWeight]}}
        for file in os.listdir(os.path.join('DEV', folder)):
            if folder == '.DS_Store':           
                continue
            with open(os.path.join('DEV', folder, file), 'r') as f:
                data = json.load(f)
                content = data['content']
                URL = data['url']
            
            files_count += 1
            docNum = len(DocIDtoURL)
            DocIDtoURL[docNum] = URL
            content = BeautifulSoup(content, 'lxml')
            text = content.getText()
            tokens = tokenizer.tokenize(text)
            Pstemmer = PorterStemmer()

            HighVal = set() #words in bold, titles and first 3 headers
            MidVal = set() #words in  all other headers
            LowVal = set() #words that are special within the text (italicized, emphsized)

            #Retrieving Important words in first header and title
            for item in content.find_all(["h1", "title", "h2", "h3", "b"]):
                stems = [Pstemmer.stem(x) for x in tokenizer.tokenize(item.text)]
                for s in stems:
                    HighVal.add(s)

            #Retrieving Important words in other headers
            for item in content.find_all(["h4", "h5", "h6"]):
                stems = [Pstemmer.stem(x) for x in tokenizer.tokenize(item.text)]
                for s in stems:
                    MidVal.add(s)

            #Retrieving Important words in text content including: (bold, italicized, emphasized)
            for item in content.find_all(["i", "em"]):
                stems = [Pstemmer.stem(x) for x in tokenizer.tokenize(item.text)]
                for s in stems:
                    LowVal.add(s)

            weight = 0
            for token in tokens:
                stem = Pstemmer.stem(token)
                Allunique.add(token)
                if stem in HighVal:
                    weight = 5
                elif stem in MidVal:
                    weight = 3
                elif stem in LowVal:
                    weight = 1
                else:
                    pass
                
                if stem not in indexes:
                    indexes[stem] = {docNum:[1, weight]}
                elif stem in indexes and docNum not in indexes[stem]:
                    indexes[stem][docNum] = [1, weight]
                elif stem in indexes:
                    indexes[stem][docNum][0] += 1 * weight
                    indexes[stem][docNum][1] = weight
                else: pass

            if files_count > 18463 and stored_indices == 0:
                with open("index1.json", 'w', encoding='utf-8') as f:
                    json.dump(indexes, f)
                    indexes.clear()
                    files_count = 0
                    stored_indices+= 1

            elif files_count > 18463 and stored_indices == 1:
                with open("index2.json", 'w', encoding='utf-8') as f:
                    json.dump(indexes, f)
                    indexes.clear()
                    files_count = 0
                    stored_indices += 1
            
            elif files_count > 18463 and stored_indices == 2:
                with open("index3.json", 'w', encoding='utf-8') as f:
                    json.dump(indexes, f)
                    indexes.clear()
                    files_count = 0
                    stored_indices += 1
            else:
                pass
    main = dict()
    for index in ["index1.json", "index2.json", "index3.json"]:
        with open("Brain.json", 'r', encoding='utf-8') as brain:
            main = json.load(brain)

        with open(index, 'r', encoding='utf-8') as f:
            Pindex = json.load(f)
            for token, posting in Pindex.items():
                if token in main:
                    main[token].update(posting)
                else:
                    main[token] = posting

        with open('Brain.json', 'w', encoding='utf-8') as f:
            for key, val in sorted(main.items(), key=lambda i:i[0]):
                f.write("{"+key+": " + str(val) + "\n" )

    with open('Brain.json', 'r', encoding='utf-8') as p:
        brain = json.load(p)
        count = 0
        for token, _ in brain.items():
            Term_index[token] = count
            ++count

    with open('term_index.json', 'w', encoding='utf-8') as ti:
        json.dump(Term_index,ti)


    with open("DocNumtoURL_Dict_.json", 'w', encoding='utf-8') as f:
        json.dump(DocIDtoURL, f)


if __name__ == '__main__':
    indexer()

    print("Number of Documents: " + str(len(DocIDtoURL)))
    print("Unique Tokens: " + str(len(Allunique)))