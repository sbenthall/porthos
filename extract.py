#! /usr/bin/env python

from __future__ import print_function
import cPickle
import sys

def main():
    prefix="."
    if len(sys.argv)>1:
        prefix=sys.argv[1]
    prefix=prefix+"/"
    print("Extracting in", prefix)
    db=cPickle.load(open('data-all.db', 'r'))
    for key in db:
        if 'lang' in db[key]:
            if db[key]['lang']=='en':
                print(db[key]['clean'].encode('utf8'), 
                      file=open(prefix+str(db[key]['label'])+" "+key+".txt", "w"))
    exit(0)

if __name__ == "__main__":
    main()
