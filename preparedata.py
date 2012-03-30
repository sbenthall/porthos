import re
from settings import *
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
import os
import simplejson as json


TOPICS_PATTERN = "(\d*) %s\/([01]) (?:\w*.txt) ([ .\d]*)" % (DATA_DIR)
TOPIC_PATTERN = "(\d*) (0\.\d*)"

def parse_topics():
    ''' Returns an M by N array, where M is number of tweets, N is number of topics, and A[m,n] is the value of the m'th topic for the n'th tweet. '''

    inferred_topics_string = open(INFERRED_FILE,'r').read()
    matches = re.findall(TOPICS_PATTERN, inferred_topics_string)
    num_matches = len(matches)

    topic_data = zeros((num_matches,NUM_TOPICS))
    spam_data = zeros(num_matches)

    for i,(index,spam,topics) in enumerate(matches):
        spam_data[i] = spam

        tm = re.findall(TOPIC_PATTERN,topics)

        for topic, value in tm:
            # WARNING: indices of matrix do not
            # match indices in inferred topics
            # document, because there
            # are failed regex matches
            topic_data[i,int(topic)] = float(value)

    return topic_data, spam_data
def main():

    print "Starting to prepare data"

    tweet_topic_matrix, spam_matrix = parse_topics()
    print tweet_topic_matrix, spam_matrix
    numpy.save('tweet_topic_matrix',tweet_topic_matrix)
    numpy.save('spam_matrix',spam_matrix)
    print "Saved tweet_topic_matrix"

if __name__ == "__main__":
    main()
