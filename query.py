import json
import tokenizer
import ast
import math
import time
from nltk.stem import PorterStemmer

stopWords = set(stopwords.words('english'))
PS = PorterStemmer()
def retrieval(query):
    global stopWords
    global PS
    results = dict()
    query_tokens = tokenizer.tokenize(query)
    while True:
        if len(query) <= 0:
            print("Goodbye")
            break
        #tokenize query and then check if it contains mostly stopwords
        #return query w/o stop words if stop words to token ratio is less than 3/4 of query
        #else return all words in query
        query_tokens = tokenizer.tokenize(query)
        Stops = 0
        tokes = 0
        related_docs = []
        for item in query_tokens:
            if item in stopWords:
                Stops += 1
            tokes += 1
        if (Stops / tokes) <= 0.75:
            tokens = [PS.stem(x) for x in query_tokens]
        else:
            tokens = [PS.stem(x) for x in query_tokens if x not in stopWords]

        with open('Brain.json', 'r', encoding='utf-8') as brain:
            with open('term_index.json', 'r', encoding='utf-8') as ti:
                term_index = json.load(ti)
                for item in tokens:
                    try:
                        index = term_index[item]
                        brain.seek(index)
                        info = brain.readline()
                        print(info)
                        related_docs.append()
                    except:
                        pass
            index1 = json.load(brain)
            
        if len(related_docs) == 0:
            print(f"Your search - '{query}' - did not match any documents")
            break
        
        intersections = related_docs[0].intersection(*related_docs)
        if len(intersections) == 0:
            break
        for item in intersections:
            for token in tokens: #calculating tf_idf_score of each token
                tf_idf_score_pt = (1 + math.log(index1[token][item][0], 10)) * math.log(55393 / len(index1[token]), 10)
                if item in results:
                    results[item] += tf_idf_score_pt
                else:
                    results[item] = tf_idf_score_pt

        results = dict(sorted(results.items(), key = lambda item: item[1], reverse=True))

        with open(r'DocNumtoURL_Dict_.json', 'r', encoding='utf-8') as f:
            URLs = json.load(f)
            print(f"Top 10 Results from Search: \"{query}\"")
            for index, x in enumerate(results):
                print(f"{index}. {URLs[int(x)]}")

        break




if __name__ == "__main__":
        start_time = int(round(time.time() * 1000))
        query = input("Enter Query")
        retrieval(query)
        end_time = int(round(time.time() * 1000)) # end of timer
        time_lapsed = end_time - start_time
        print()
        print(f'{time_lapsed}ms')