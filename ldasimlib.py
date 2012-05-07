# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import cPickle
import gensim
import re
import text_processing
reload(text_processing)
stopwords=text_processing.stopwords
from text_processing import to_bow
from zlib import decompress
from numpy import random, mean, save
from numpy import array,zeros,ones,dot
from math import sqrt
from pylab import hist, legend, title, xlabel, ylabel, show, savefig, clf
import itertools

#set of interesting htmls to consider
def candidates(html,w2i):
    candidates = set()
    
    for key in html:
        for comp in html[key]:
            bag=to_bow(decompress(comp), w2i)
            if len(bag)>0:
                if key not in candidates:
                    candidates.add(key)

    return candidates

def to_nbow(text,w2i):
    return [[w2i[x[0]], x[1]] for x in to_bow(text, w2i).items() if x[0] not in stopwords]

## TODO: rewrite for streaming
## -- see gensim documentation for how to build this
def build_corpus(candidates,w2i,cutoff=10000):
    random.seed(0)
    candidates=random.permutation(list(candidates))
    corpus=[]
    for key in pcandidates[:cutoff]:
        for comp in html[key]:
            corpus.append(to_nbow(decompress(comp)),w2i)
    return corpus

#compute cosine similarity of two vectors x and y
def cosine(x, y):
    if len(x) == 0 or len(y) == 0:
        return 0

    Nx=0
    Ny=0
    num=0
    j=0
    i=0
    while i < len(x):
        if j < len(y):
            if x[i][0]==y[j][0]:
                num += x[i][1]*y[j][1]
                Nx+=x[i][1]**2
                Ny+=y[j][1]**2
                i+=1
                j+=1
                continue
            if x[i][0]<y[j][0]:
                Nx+=x[i][1]**2
                i+=1
                continue
            if x[i][0]>y[j][0]:
                Ny+=y[j][1]**2
                j+=1
                continue
        else:
            Nx+=x[i][1]**2
            i+=1
    while j < len(y):
        Ny+=y[j][1]**2
        j+=1
    return num/sqrt(Nx*Ny)

# computes topic vector cosine similarity of
# two bags of words, given an LDA model
def lda_cosine(tw,ht,model):
    d = []
    for i in range(20):
        twv=model[tw]
        htv=model[ht]
        d.append(cosine(twv, htv))
    return mean(d)    

# compute jaccard similarity between two bags of words
def jaccard(tw,ht,model='dummy'):
    tw_keys = set([p[0] for p in tw])
    ht_keys = set([p[0] for p in ht])    
    return float(len(tw_keys & ht_keys)) / len(tw_keys | ht_keys)

# compute TF-IDF cosine similarity between two bags of words
def tfidfcosine(tw,ht,tfidfmodel):
    return cosine(sorted(tfidfmodel[tw]),sorted(tfidfmodel[ht]))

# returns a dictionary with keys from the 
# tweets dictionary and values that are
# tuples with tweet and HTML bags of words
#
# keys are ignored if tweets or HTML do
# not contain useful information
def filter_tweets(tweets,html,w2i,cutoff=1000):
    good_tweet_bags = {}
    k = 0
    for key in tweets:
        k+=1
        if k > cutoff:
            break
        if tweets[key]['lang_infered']=='en':
            if key in html:
                tw=to_nbow(tweets[key]['text_clean'],w2i)
                if len(tw)>= 1 and len(html[key])>0: 
                    ht=to_nbow(decompress(html[key][0]),w2i)
                    if len(ht)>=1:
                        good_tweet_bags[key] = {
                            "is_spam": tweets[key]['label']==1,
                            "tw": tw,
                            "ht": ht 
                            }
    return good_tweet_bags

def ham_spam_similarities(tweet_bags,bow_sim,tweets,model='dummy'):
    k=0
    spam=[]
    ham=[]
    for key in tweet_bags:
        tw = tweet_bags[key]["tw"]
        ht = tweet_bags[key]["ht"]
        sim = bow_sim(tw,ht,model)
        if tweet_bags[key]["is_spam"]:
            spam.append(sim)
        else:
            ham.append(sim)
    return ham,spam


def make_cdf(ham,spam,similarity_name):
    hist(ham, alpha=0.5, bins=100, normed=True, cumulative=True, histtype='stepfilled', label='Ham ('+str(len(ham))+')', color='b')
    hist(spam, alpha=0.5, bins=100, normed=True, cumulative=True, histtype='stepfilled', label='Spam ('+str(len(spam))+')', color='r')
    legend(loc=2)
    title("CDF of %s similarity for spam and ham" % (similarity_name))
    xlabel("%s similarity" % (similarity_name))
    ylabel("proportion")
    savefig("%s_cdf.png" % similarity_name)
    show()
    clf()

