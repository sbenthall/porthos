from __future__ import print_function, division
import sys, re, ujson, tarfile
from pprint import pprint
from traceback import print_exc
from text_processing import normalize, twochars
from html2text import bytes_to_text
import cPickle
from multiprocessing import Pool
from unidecode import unidecode
from zlib import compress

def fparse(kv):
    return kv[0], compress(unidecode(normalize(bytes_to_text(kv[1]).lower())))

def do_clean(pool, queue_size=2000):
    tweetinfo=cPickle.load(open('tweets+.db', 'r'))

    tar=tarfile.open('../sample.tar.gz', 'r:gz')
    i=0
    html=dict()
    inputs=[]
    results_last = None
    for tarinfo in tar:
        if tarinfo.name[-9:-4]=='tweet':
            key=tarinfo.name[-42:-10]
            if key in tweetinfo and tweetinfo[key]['lang_infered']=='en':
                html[key]=[]
                try:
                    data=ujson.loads(tar.extractfile(tarinfo).read())
                    for win in data['windows']:
                        if len(inputs)<queue_size:
                            inputs.append((key, win['html']))
                        else:
                            results = pool.map_async(fparse, inputs)
                            if results_last is not None:
                                for key, value in results_last.get():
                                    html[key].append(value)
                            results_last = results
                            inputs=[]
                except:
                    print_exc()
            if i%1000 ==0:
                print(i, end=' ', file=sys.stderr)
            i+=1
    for key, value in results_last.get():
        html[key].append(value)
    return html

if __name__ == '__main__':
    pool = Pool(processes=8)
    html=do_clean(pool)
    cPickle.dump(html, open('html.db', 'w'))
