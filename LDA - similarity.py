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

# <codecell>

i2w, w2i = cPickle.load(open('i2w-w2i.db','r'))
html=cPickle.load(open('html.db', 'r'))

# <codecell>

candidates=set() #set of interesting htmls to consider
for key in html:
    for comp in html[key]:
        bag=to_bow(decompress(comp), w2i)
        if len(bag)>0:
            if key not in candidates:
                candidates.add(key)

# <codecell>

random.seed(0)
pcandidates=random.permutation(list(candidates))

# <codecell>

def to_nbow(text):
    return [[w2i[x[0]], x[1]] for x in to_bow(text, w2i).items() if x[0] not in stopwords]

# <codecell>

corpus=[]
for key in pcandidates[:10000]:
    for comp in html[key]:
        corpus.append(to_nbow(decompress(comp)))

# <codecell>

model=gensim.models.ldamodel.LdaModel(corpus, id2word=i2w, num_topics=100)

# <codecell>

tweets=cPickle.load(open('tweets+.db', 'r'))

# <codecell>

tweets.keys()[:10]

# <codecell>


# <codecell>

b=model[to_nbow(decompress(html['94041daa43fc3dca1a3582119b74b4a7'][0]))]

# <codecell>

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

# <codecell>

k=0
spam=[]
ham=[]
for key in tweets:
    if tweets[key]['lang_infered']=='en':
        if key in html:
            tw=to_nbow(tweets[key]['text_clean'])
            if len(tw)<1:
                continue
            if len(html[key])>0:
                    ht=to_nbow(decompress(html[key][0]))
                    if len(ht)<1:
                        continue
            else:
                continue
            d=[]
            for i in range(50):
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

# <codecell>

hist(ham, alpha=0.5, bins=50, normed=True, cumulative=False, histtype='stepfilled', label='Ham ('+str(len(ham))+')', color='b')
hist(spam, alpha=0.5, bins=50, normed=True, cumulative=False, histtype='stepfilled', label='Spam ('+str(len(spam))+')', color='r')
legend(loc=2)
title("CDF of cosine similarity for spam and ham")
xlabel("cosine similarity")
ylabel("proportion")

# <codecell>

for key in tweets:
    if tweets[key]['lang_infered']=='en':
        if tweets[key]['label']==0:
            print(tweets[key]['text_original'])

# <codecell>

save('gammas-spam-ham', full_matrix)
save('labels', labels)

# <codecell>

[i2w[x[0]] for x in corpus[0]]

# <codecell>

model_all.show_topics(25)

# <codecell>

len(stopwords)

# <codecell>

stopwords

# <codecell>


