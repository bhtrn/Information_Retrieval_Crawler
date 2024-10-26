import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.robotparser
from collections import defaultdict

explored_urls = set()

domains = defaultdict(int)

word_count = defaultdict(int)

unique_links = set()

longest_page = {'link': '', 'length': 0}

STOPWORDS = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j", "just", "k", "keep	keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure	t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "z", "zero"]

def tokenize(url, resp):
    global word_count
    global STOPWORDS
    tokens = []
    parsed = BeautifulSoup(resp.raw_response.content, "html.parser")
    # Gets text from parsed HTML
    text = parsed.get_text(" ")
    
    # Removed puncuation
    res = re.sub(r'[^\w\s]', '', text)  
    words = res.split()
    # Iterates through all relevant words and appends them to a list if they are ASCII valid.
    for word in words:
        if all(ord(c) < 128 for c in word):     
            tokens.append(word.lower())   
            if word not in STOPWORDS:
                word_count[word.lower()] += 1   

    return tokens


def check_length(url, resp):
    global longest_page
    parsed = BeautifulSoup(resp.raw_response.content, "html.parser")
    text = parsed.get_text(" ")

    text = text.split()
    if len(text) > longest_page['length']:
        longest_page['link'] = resp.url
        longest_page['length'] = len(text)
        

def check_domain(parsed):
    #URLS to crawl
    url = parsed.geturl()
    URLS = ['ics.uci.edu/', 'cs.uci.edu/', 'informatics.uci.edu/', 'stat.uci.edu/', 'today.uci.edu/department/information_computer_sciences/']
    try:  
        # Checks if targeted domains are in url
        if URLS[0] in url or URLS[1] in url or URLS[1] in url or URLS[1] in url or URLS[1] in url:
            return True
        else: return False
    except:
        return False
    

def check_quality(url, resp):
    global stopwords
    try:      
        tokens = tokenize(url, resp)
        relevant = set()
        rel = 0
        count = 0
        # Adds relevant words into a set containing relevent words.
        for token in tokens:
            if token not in stopwords:
                relevant.add(token)
                rel += 1
            else: count += 1
        
        # if there are 2x the amount of stopwords.
        if rel <= count / 2: return False
        
        # If file is over 80000 words, return False.
        if len(tokens) > 80000: return False
        
        # if more than 200 unique relevant words, return True.
        if len(relevant) > 200: return True
        else: return False
    except: return False


def check_traps(parsed_url):
    global domains
    # Long invalid URL trap
    if len(str(parsed_url.geturl())) > 250:
        return False
    
    # Repeating dictionary - taken from https://support.archive-it.org/hc/en-us/articles/208332963-How-to-modify-your-crawl-scope-with-a-Regular-Expression
    if re.match("^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed_url.path):
        return False
    
    # Extra dictionaries - taken from https://support.archive-it.org/hc/en-us/articles/208332963-How-to-modify-your-crawl-scope-with-a-Regular-Expression
    if re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$", parsed_url.path):
        return False
    
    # Calendars
    if 'calendar' in parsed_url.geturl() or 'event' in parsed_url.geturl() or '#' in parsed_url.geturl() or 'evoke' in parsed_url.geturl() or 'action' in parsed_url.query:
        return False
        
    domains[parsed_url.netloc] += 1
    if domains[parsed_url.netloc] > 300: return False
    

    

    return True


def check_robot(url, rob_url):
    # Reads content of robots.txt file - code referenced from https://docs.python.org/3/library/urllib.robotparser.html
    try:
        robot_url = "http://" + rob_url + "/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robot_url)
        rp.read()
        
        return rp.can_fetch("*", url)
    except: return False


def scraper(url, resp):

    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]



def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    
    # Return empty list if server returns error status.
    try:

        if resp.status != 200: return []
        
        #Checks quality of page
        #if not check_quality(url, resp): return []
        
        # List of urls to return.
        pages = set()  
        parsed = BeautifulSoup(resp.raw_response.content, "html.parser")   
            
        # list of all links parsed on the page.
        links = parsed.find_all('a')
        
        # Loops through all links and checks their validity.
        for link in links:  
            href = link.get('href')
            pages.add(href)
            check_length(link, resp)


    except:
        pass
    return list(pages)


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    global explored_urls

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #Checks if domain is one of the five specified domains to scrape.     
        if not check_domain(parsed): return False
        
        
        # # # Checks if url has already been explored.
        if url in explored_urls: return False
        else: explored_urls.add(url)
    

        # # # Checks for traps.
        if not check_traps(parsed): return False
        
              
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


def print_report():
    global explored_urls
    global longest_page
    global word_count
    global domains
    #Prints report
    print('1. ', len(explored_urls))
    print('2. ', longest_page['link'], longest_page['length'])
    most_common = sorted(word_count, key=lambda x: x[1], reverse=True)
    print('3. ', most_common)
    subdomains = sorted(domains)
    print('4. ')
    for dom in subdomains:
        print(dom, domains[dom])