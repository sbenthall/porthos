# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from __future__ import print_function, division
import sys, re, ujson, tarfile
from pprint import pprint
from traceback import print_exc
from language_detector import guess
from text_processing import normalize
from url_detector import replaceURLs, getURLs
import cPickle
from datetime import date
from HTMLParser import HTMLParser

# <codecell>

pAt=re.compile(r"\@\w+")
extras=re.compile(r"[0-9\#\=\?\!\(\)\\\/\>\<\_\@\$\^\&\%\`\~\+\]\[\}\{]+")
p=HTMLParser()
unescape=p.unescape

def process_raw_text(text):
    return normalize(extras.sub('', pAt.sub('', replaceURLs('', text)))).strip()

# <codecell>

label=dict()
with open('sample_index.txt', 'r') as index:
    for line in index:
        if line[-10:-5]=='tweet':
            label[line[-43:-11]]=int(line[0])

# <codecell>

tar=tarfile.open('../sample.tar.gz', 'r:gz')
i=0
stats=dict()
for tarinfo in tar:
    if tarinfo.name[-9:-4]=='tweet':
        try:
            key=tarinfo.name[-42:-10]
            data=ujson.loads(tar.extractfile(tarinfo).read())
            ts=data['tweet']['fulltweet']['created_at']
            raw_text=data['tweet']['fulltweet']['text']
            stats[key]={'ts': ts,
                        'lang_tweeter': data['tweet']['fulltweet']['user']['lang'],
                        'text_original': raw_text,
                        'label': label[key]}
            #for win in data['windows']:
            #    html=win['html']
            #    x=bytes_to_bow(html)
            if i%1000 ==0:
                print(i, end=' ', file=sys.stderr)
            i+=1
        except:
            print_exc()
            print("Could not process:", tarinfo.name, file=sys.stderr)

# <codecell>

cPickle.dump(stats, open('tweets.db', 'w'))

# <codecell>

mapping={'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

for key in stats:
    ts=stats[key]['ts'].split(' ')
    stats[key]['date']=date(day=int(ts[2]), month=mapping[ts[1]], year=int(ts[-1]))
    stats[key]['text_original_u']=unescape(stats[key]['text_original'])
    stats[key]['text_clean']=process_raw_text(stats[key]['text_original_u'])
    stats[key]['lang_infered']=guess(stats[key]['text_clean'].encode('utf8'))[0][0]

# <codecell>

cPickle.dump(stats, open('tweets+.db', 'w'))

# <codecell>

counts={}
counts_ham={}
counts_spam={}
for key in stats:
    d=stats[key]['date']
    if d in counts:
        counts[d]+=1
    else:
        counts[d]=1
    if stats[key]['label'] == 0:
        if d in counts_ham:
            counts_ham[d]+=1
        else:
            counts_ham[d]=1
    if stats[key]['label'] == 1:
        if d in counts_spam:
            counts_spam[d]+=1
        else:
            counts_spam[d]=1

# <codecell>

N, Nh, Ns = sum(counts.values()), sum(counts_ham.values()), sum(counts_spam.values())

x=array(counts.keys())
y=array(counts.values())
ix=argsort(x)

xh=array(counts_ham.keys())
yh=array(counts_ham.values())
ixh=argsort(xh)

xs=array(counts_spam.keys())
ys=array(counts_spam.values())
ixs=argsort(xs)

semilogy(x[ix], y[ix], '-', label="Total 218,671", color='b')
semilogy(xs[ixs], ys[ixs], '-', label="Spam 171,110 (78%)", color='r')
semilogy(xh[ixh], yh[ixh], '-', label="Ham 47,561 (22%)", color='g')
legend(loc=0)
ylabel("Number of tweets (log scale)")
title("Number of tweets per day")

# <codecell>

cl=[len(stats[key]['text_original_u']) for key in stats]
ol=[len(stats[key]['text_clean']) for key in stats]
hist(ol, bins=arange(141)/141*140, alpha=0.5, label='Clean content', histtype='stepfilled', normed=True, cumulative=True)
hist(cl, bins=arange(141)/141*140, alpha=0.5, label='Raw content', histtype='stepfilled', normed=True, cumulative=True)
ylim(0,1)
xlabel("Number of characters")
ylabel("Proportion")
title("CDF of number of characters")
legend(loc=2)

# <codecell>

count_lang_i=dict()
count_lang_t=dict()
for key in stats:
    li=stats[key]['lang_infered']
    lt=stats[key]['lang_tweeter']
    if li not in count_lang_i:
        count_lang_i[li]=0
    count_lang_i[li]+=1
    if lt not in count_lang_t:
        count_lang_t[lt]=0
    count_lang_t[lt]+=1

# <codecell>

i=0
for key in stats:
    if stats[key]['lang_infered']=='en' and stats[key]['lang_tweeter']!='en':
        print(stats[key]['text_clean'])
    i+=1

# <codecell>

count_lang_t

# <codecell>

tlang=array(count_lang_t.keys())
tcounts=array(count_lang_t.values())
ix=argsort(tcounts)[::-1]
tlang=tlang[ix]
tcounts=tcounts[ix]
explode=(0.05, 0, 0, 0, 0, 0)

pie(tcounts, explode= explode, labels=tlang, autopct='%1.1f%%', shadow=False)
title("Languages [Twitter]")

# <codecell>

count={}
count['other']=0
for l in count_lang_i:
    if l in other:
        count['other']+=count_lang_i[l]
    else:
        count[l]=count_lang_i[l]

tlang=['en', 'jp', 'por', 'spa', 'ger', 'fr', 'other']
labels=[]
for l in tlang:
    labels.append(l+" ("+str(int(count_type[l][1]/(count_type[l][1]+count_type[l][0])*100))+"% spam)")
tcounts=[count[l] for l in tlang]
explode=[0.05]+[0]*(len(tcounts)-1)

pie(tcounts, explode= explode, labels=labels, autopct='%1.1f%%', shadow=False)
title("Languages [compression method]")

# <codecell>

other=['taga', 'swe', 'dut', 'ru', 'it', 'cn', 'fin', 'gre', 'esper', 'latin']
count_type=dict()
count_type['other']=dict()
for key in stats:
    l=stats[key]['lang_infered']
    s=stats[key]['label']
    if l in other:
        d=count_type['other']
    else:
        if l in count_type:
            d=count_type[l]
        else:
            count_type[l]=dict()
            d=count_type[l]
    if s in d:
        d[s]+=1
    else:
        d[s]=1
    

# <codecell>


# <codecell>


