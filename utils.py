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
            print("Oops", tarinfo.name, file=sys.stderr)

import cPickle
cPickle.dump((label, files), open('raw_tweets.db', 'w'))

# <markdowncell>

# Conversion after the fact

# <codecell>

label, files=cPickle.load(open('raw_tweets.db', 'r'))

# <codecell>

data=dict()
for id in label:
    data[id]=dict()
    if id not in files:
        print("Missing", id)
        continue
    data[id]['lang']=files[id][0]
    data[id]['raw']=files[id][1]
    data[id]['clean']=process_raw_text(files[id][1]).replace('\'', '')
    data[id]['label']=label[id]

# <codecell>

cPickle.dump(data, open('data-all.db', 'w'))

# <codecell>


