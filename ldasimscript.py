from ldasimlib import *
import cPickle
import gensim
from zlib import decompress


HTML_DATA = 'html.db'

print 'Loading data'

i2w, w2i = cPickle.load(open('i2w-w2i.db','r'))
html=cPickle.load(open('html.db', 'r'))

#print 'Computing candidates'
#candidates = candidates(html,w2i)

#print 'Building corpus'

#corpus = build_corpus(candidates)
#print 'Saving corpus'
#cPickle.dump(corpus,open('corpus.pkl','w'))

print 'Loading corpus'
corpus = cPickle.load(open('corpus.pkl','r'))

#print 'Generating model'
#model=gensim.models.ldamodel.LdaModel(corpus, id2word=i2w, num_topics=100)

#print 'Saving model'
#model.save('model.pkl')

print 'Loading LDA model'
model = gensim.models.ldamodel.LdaModel.load('model.pkl')

print 'Generating TF-IDF model'
tfidfmodel = gensim.models.tfidfmodel.TfidfModel(corpus)

print 'Loadinging tweets'
tweets=cPickle.load(open('tweets+.db', 'r'))

print 'Filtering tweets'
            
tweet_bags = filter_tweets(tweets,html,w2i,cutoff=2000)
cPickle.dump(tweet_bags,open('tweet-bags.pkl','w'))

print 'Computing similarities with LDA Cosine'
ham,spam = ham_spam_similarities(tweet_bags,lda_cosine,tweets,model)
make_cdf(ham,spam, 'lda cosine')

print 'Computing similarities with Jaccard'
ham,spam = ham_spam_similarities(tweet_bags,jaccard,tweets)
make_cdf(ham,spam, 'Jaccard')

print 'Computing similarities with TFIDF Cosine'
ham,spam = ham_spam_similarities(tweet_bags,tfidfcosine,tweets,tfidfmodel)
make_cdf(ham,spam, 'tf-idf cosine')


