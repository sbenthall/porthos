import nltk
import numpy
import random

#print "Loading data from matrices"
#ttm = numpy.load("tweet_topic_matrix.npy")
#sm = numpy.load("spam_matrix.npy")

N = 4
TRAINING_RATIO = .9

class LdaSpamClassifierTester:
    
    # ttm, htm, and sm are numpy arrays
    # ttm - tweet topic matrix
    # htm - html topic matrix
    # sm - spam matrix (i.e., sm[i] is 1 iff tweet i is spam
    def __init__(self,ttm,htm,sm):
        self.ttm = ttm
        self.htm = htm
        self.sm = sm
    
    def features(self,i):
        return dict([t for t in enumerate(self.ttm[i,:])])

    def training_example(self,i):
        label = "spam" if self.sm[i] else "ham"
        return (self.features(i), label)

    def sample_indices(self,training_ratio=TRAINING_RATIO):
        n_training = int(self.sm.size * training_ratio)
        print "Training on %s, Testing on %s" % (n_training, self.sm.size)
        print "Selecting training and testing indices"
        permuted_indices = numpy.random.permutation(self.sm.size)
        training_indices = numpy.arange(self.sm.size)[permuted_indices[n_training:]]
        testing_indices = numpy.arange(self.sm.size)[permuted_indices[:n_training]]
        return training_indices, testing_indices

        #train classifier on specified indices of the training set
    def train(self,training_indices):
        # using all data for now
        training_set = [self.training_example(i) for i in training_indices]
    
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        return classifier

    def test(self,classifier, testing_indices):
        testing_set = [(self.features(i)) for i in testing_indices]
        test_results = classifier.batch_classify(testing_set)
    
        accurate_test_results = [label == ('spam' if self.sm[testing_indices[i]] else 'ham') for i,label in enumerate(test_results)]
        return test_results, accurate_test_results

    def ratio(self,data):
        return float(sum(data)) / len(data)

    def compute_classifier_success(self,n_for_validation=N):
        ratios = []

        for n in range(N):
            train_i, test_i = self.sample_indices()
            classifier = self.train(train_i)
            results, accuracy = self.test(classifier, test_i)
            
            print self.ratio(accuracy)
            ratios.append(self.ratio(accuracy))
                
        mean_success = numpy.mean(ratios)
        
        print "Average ratio: " + str(mean_success)
        print "Spam rate: " + str(0.0 + sum(self.sm) / self.sm.size )
        
        return mean_success
