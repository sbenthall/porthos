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
from numpy import random, mean
from math import sqrt

HTML_DATA = 'html.db'

print 'Loading data'

i2w, w2i = cPickle.load(open('i2w-w2i.db','r'))
html=cPickle.load(open('html.db', 'r'))

#print 'Computing candidates'
#set of interesting htmls to consider
def candidates(html):
    candidates = set()
    
    for key in html:
        for comp in html[key]:
            bag=to_bow(decompress(comp), w2i)
            if len(bag)>0:
                if key not in candidates:
                    candidates.add(key)

    return candidates

#candidates = candidates(html)

#print 'Permuting candidates'
#random.seed(0)
#pcandidates=random.permutation(list(candidates))

#print 'Building corpus'

def to_nbow(text):
    return [[w2i[x[0]], x[1]] for x in to_bow(text, w2i).items() if x[0] not in stopwords]

def build_corpus(pcandidates):
    corpus=[]
    for key in pcandidates[:10000]:
        for comp in html[key]:
            corpus.append(to_nbow(decompress(comp)))
    return corpus

#corpus = build_corpus(pcandidates)
#print 'Saving corpus'
#cPickle.dump(corpus,open('corpus.pkl','w'))

print 'Loading corpus'
corpus = cPickle.load(open('corpus.pkl','r'))

#print 'Generating model'
#model=gensim.models.ldamodel.LdaModel(corpus, id2word=i2w, num_topics=100)

#print 'Saving model'
#model.save('model.pkl')

print 'Loading model'
model = gensim.models.ldamodel.LdaModel.load('model.pkl')

print 'Loadinging tweets'
tweets=cPickle.load(open('tweets+.db', 'r'))

print tweets.keys()[:10]

print model[to_nbow(decompress(html['94041daa43fc3dca1a3582119b74b4a7'][0]))]

#compute cosine similarity of two vectors x and y
def cosine(x, y):
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

def filter_tweets(tweets):
    good_tweet_bags = {}
    for key in tweets:
        if tweets[key]['lang_infered']=='en':
            if key in html:
                tw=to_nbow(tweets[key]['text_clean'])
                if len(tw)<1: # no good words in tweet
                    continue
                if len(html[key])>0: 
                    ht=to_nbow(decompress(html[key][0]))
                    good_tweet_bags[key] = (tw,ht)
                    if len(ht)<1:
                        continue # no information in html
            else:
                continue
    return good_tweet_bags
            
tweet_bags = filter_tweets(tweets)    
k=0
spam=[]
ham=[]
for key in tweets:
    if tweets[key]['lang_infered']=='en':
        if key in html:
            tw=to_nbow(tweets[key]['text_clean'])
            if len(tw)<1: # no good words in tweet
                continue
            if len(html[key])>0: 
                    ht=to_nbow(decompress(html[key][0]))
                    if len(ht)<1:
                        continue # no information in html
            else:
                continue
            d=[]
            for i in range(20):
                twv=model[tw]
                htv=model[ht]
                d.append(cosine(twv, htv))
            if tweets[key]['label']==1:
                spam.append(mean(d))
            else:
                ham.append(mean(d))
            if k>1000:
                break
            k+=1
        else:
            continue

hist(ham, alpha=0.5, bins=50, normed=True, cumulative=False, histtype='stepfilled', label='Ham ('+str(len(ham))+')', color='b')
hist(spam, alpha=0.5, bins=50, normed=True, cumulative=False, histtype='stepfilled', label='Spam ('+str(len(spam))+')', color='r')
legend(loc=2)
title("CDF of cosine similarity for spam and ham")
xlabel("cosine similarity")
ylabel("proportion")


for key in tweets:
    if tweets[key]['lang_infered']=='en':
        if tweets[key]['label']==0:
            print(tweets[key]['text_original'])


save('gammas-spam-ham', full_matrix)
save('labels', labels)


[i2w[x[0]] for x in corpus[0]]

model_all.show_topics(25)

len(stopwords)

stopwords


