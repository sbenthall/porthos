from ldasimlib import *
import cPickle
import gensim
import classify
from zlib import decompress


HTML_DATA = 'html.db'

print 'Loading data'

i2w, w2i = cPickle.load(open('i2w-w2i.db','r'))
html=cPickle.load(open('html.db', 'r'))

#print 'Loading corpus'
#corpus = cPickle.load(open('corpus.pkl','r'))
#print 'Saving model'
#model.save('model.pkl')
#print 'Loading LDA model'
#ldamodel = gensim.models.ldamodel.LdaModel.load('model.pkl')

print 'Loading tweets'
tweets=cPickle.load(open('tweets+.db', 'r'))

print 'Filtering tweets'
tweet_bags = filter_tweets(tweets,html,w2i,cutoff=5000)
cPickle.dump(tweet_bags,open('tweet-bags.pkl','w'))

#print 'Computing similarities with Jaccard'
#ham,spam = ham_spam_similarities(tweet_bags,jaccard,tweets)
#make_cdf(ham,spam, 'Jaccard')

def ldasimtest(num_topics):
    #print 'Generating model'
    ldamodel=gensim.models.ldamodel.LdaModel(build_corpus_iterator(html,w2i), id2word=i2w, num_topics=num_topics)

    cPickle.dump(ldamodel,"LDAmodel-%dt.pkl" % (num_topics))

    print 'Generating Numpy arrays for spam, tweet topics, and html topics'
    tweet_topic_data, html_topic_data, spam_data = tweet_bags2ldanpy(tweet_bags,ldamodel,num_topics=num_topics)

    print 'Creating LdaSpamClassifier object for testing classifiers'
    classifier = classify.LdaSpamClassifierTester(tweet_topic_data,spam_data)
    tweet_success = classifier.compute_classifier_success(8)

    classifier = classify.LdaSpamClassifierTester(html_topic_data,spam_data)
    html_success = classifier.compute_classifier_success(8)

    print "Tweet success: %f, HTML success: %f"%(tweet_success,html_success)

    print 'Computing similarities with LDA Cosine'
    ham,spam = ham_spam_similarities(tweet_bags,lda_cosine,tweets,ldamodel)
    make_cdf(ham,spam, 'lda cosine',file_name="ldacosine_cdf_%d"%(num_topics))

ldasimtest(5)
ldasimtest(10)
ldasimtest(20)
ldasimtest(40)
ldasimtest(80)

print 'Generating TF-IDF model'
tfidfmodel = gensim.models.tfidfmodel.TfidfModel(build_corpus_iterator(html,w2i))


print 'Computing similarities with TFIDF Cosine'
ham,spam = ham_spam_similarities(tweet_bags,tfidfcosine,tweets,tfidfmodel)
make_cdf(ham,spam, 'tf-idf cosine')


