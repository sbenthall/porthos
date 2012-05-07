import simplejson as json
import urlparse
import os
import re
import codecs

DATA_SOURCE = "../data/sample7/"
DATA_DEST = "xdocs/"

URL_REGEX = "http\://\S*"
def clean(tweet):
    clean_tweet = re.sub(URL_REGEX, '', tweet)
    clean_tweet = re.sub("[\n\r\t]",' ',clean_tweet)

    #clean out retweet 'RT'
    clean_tweet = re.sub("^RT ",'',clean_tweet)
    clean_tweet = re.sub(" rt ",' ',clean_tweet)
    clean_tweet = re.sub(" RT ",' ',clean_tweet)
    clean_tweet = re.sub(" ff ",' ',clean_tweet)
    clean_tweet = re.sub(" FF ",' ',clean_tweet)

    #remove usernames
    clean_tweet = re.sub("@(\w*)",'',clean_tweet)
    
    #collapse contractions
    clean_tweet = re.sub("'ll",'ll',clean_tweet)
    clean_tweet = re.sub("'ve",'ve',clean_tweet)
    clean_tweet = re.sub("'t",'t',clean_tweet)

    return clean_tweet

def clean_timezone(tz):
    tz = tz.replace(" ","")
    tz = tz.replace("(","")
    tz = tz.replace(")","")
    tz = tz.replace("&","")
    tz = "z0" + tz
    return tz
    

def mod_url(url):
    up = url.path
    up = up.replace("/"," u0")
    up = up.replace("-"," u0")
    up = up.replace("+"," u0")
    up = up.replace("_"," u0")
    up = up.replace("."," u0")
    return up

def remove_word(doc,word):
    return doc.replace(" " + word + " "," ")

stopwords = ['0','1','2','3','4','5','6','7','8','9','d0','d0www','d0com','d0org','d0net','u0php','u0html','u0the','u0to','u0a','u0and','u0in','u0of','u0you','u0with','u0for','u0on','u0is','u0your','u0i','u0at','u0are','u0it','u0index','u0a','u0you','u0','z0None']

def clean_doc(doc):
    for sw in stopwords:
        doc = remove_word(doc,sw)
    return doc
    

fl = os.listdir(DATA_SOURCE)

for f in fl:
    obj = json.loads(open(DATA_SOURCE + f,'r').read())
    tweet = clean(obj['tweet']['fulltweet']['text'])
    timezone = clean_timezone(str(obj['tweet']['fulltweet']['user']['time_zone']))
    up = urlparse.urlparse(obj['windows'][0]['final_url'])
    netloc = "d0" + up.netloc.replace("."," d0")
    xdoc = clean_doc(" " + u' '.join([tweet,timezone,netloc, mod_url(up)]) + " ")
    print xdoc
    nf = codecs.open(DATA_DEST + f,encoding='utf-8',mode='w')
    nf.write(xdoc)

