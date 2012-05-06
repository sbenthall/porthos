# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from __future__ import print_function, division
from pprint import pprint
import tarfile
import ujson
import re
from url_detector import replaceURLs
import sys
import cPickle
#from language_detector import guess
#reload(url_detector)

# <codecell>

pAt=re.compile(r"\@\w+")
extras=re.compile(r"[0-9\#\=\?\!\(\)\\\/\>\<\_\@\$\^\&\%\`\~\+\]\[\}\{]+")

def process_raw_text(text):
    return extras.sub('', pAt.sub('', replaceURLs('', text)))

# <codecell>

label=dict()
with open('sample_index.txt', 'r') as index:
    for line in index:
        if line[-10:-5]=='tweet':
            label[line[-43:-11]]=int(line[0])

# <codecell>

tar=tarfile.open('sample.tar')

files=dict()
i=0
for tarinfo in tar:
    if tarinfo.name[-9:-4]=='tweet':
        try:
            data=ujson.loads(tar.extractfile(tarinfo).read())
            pprint(data['windows'].keys())
            break
            lang=data['tweet']['fulltweet']['user']['lang']
            raw=data['tweet']['fulltweet']['text']
            clean=process_raw_text(raw)
            lang2=guess(clean.lower().encode('utf8'))
            files[tarinfo.name[-42:-10]]=(lang2[0][0], raw)
            #print(lang, lang2[0][0], clean)
            if i%1000 ==0:
                print(i, end=' ', file=sys.stderr)
            i+=1
        except:
            break
            print("Oops", tarinfo.name, file=sys.stderr)

#import cPickle
#cPickle.dump((label, files), open('raw_tweets.db', 'w'))

# <markdowncell>

# Conversion after the fact

# <codecell>

label, files=cPickle.load(open('raw_tweets.db', 'r'))

# <codecell>

data=dict()
for id in label:
    if id not in files:
        print("Missing", id)
        continue
    data[id]=dict()
    data[id]['lang']=files[id][0]
    data[id]['raw']=files[id][1]
    data[id]['clean']=process_raw_text(files[id][1]).replace('\'', '')
    data[id]['label']=label[id]

# <codecell>

cPickle.dump(data, open('data-all.db', 'w'))

# <codecell>

import lxml.html as lh
import urllib2
from lxml.html.clean import Cleaner
import re

p=re.compile(r"[a-zA-Z]+")
doc=lh.fromstring(data['windows'][0]['html'])
p.findall(doc.text_content().replace("'", ''))
#doc.text_content().replace("'", '')

#cleaner=Cleaner()
#path = '/html/body'
#body = doc.xpath(path)[0]

#cleaner.clean_html(body).text_content()

# <codecell>

import cPickle
from zlib import decompress

# <codecell>

html=cPickle.load(open('html.db', 'r'))

# <codecell>

html.keys()[:10]

# <codecell>

i=0
c={}
for key in html:
    if len(html[key]) > 0:
        for comp in html[key]:
            h=comp
            if h not in c:
                c[h]=0
            c[h]+=1
    if i%1000==0:
        print(i)
    i+=1

# <codecell>

numerous={}
for comp in c:
    if c[comp] > 100:
        numerous[c[comp]]=decompress(comp)

# <codecell>

from text_processing import twochars

# <codecell>

def to_bow(text, to_keep=to_keep):
    bag={}
    for w in twochars.findall(text.replace("'", '')):
        if w in to_keep:
            if w not in bag:
                bag[w]=0
            bag[w]+=1
    return bag

# <codecell>

bow={} #can not fit into memory...
for key in html:
    for comp in html[key]:
        bag=to_bow(decompress(comp))
        if len(bag)>0:
            if key not in bow:
                bow[key]=[]
            bow[key].append(bag)

# <codecell>

counts={}
for key in html:
    for comp in html[key]:
        bag=to_bow(decompress(comp))
        for w in bag:
            if w not in counts:
                counts[w]=0
            counts[w]+=bag[w]

terms=counts.keys()
terms.sort(key=lambda x: counts[x])

# <codecell>

for i in range(0,100):
    print(i, counts[terms[-i]], terms[-i])

# <codecell>

counts[terms[860000]]

# <codecell>

terms[860000]

# <codecell>

to_keep=set()
for t in counts:
    if counts[t]>=5:
        to_keep.add(t)

# <codecell>

i2w=dict()
w2i=dict()
i=0
for t in terms:
    if t in to_keep:
        i2w[i]=t
        w2i[t]=i
        i+=1

# <codecell>

cPickle.dump((i2w, w2i), open('i2w-w2i.db', 'w'))

# <codecell>

w2i['']

# <codecell>


