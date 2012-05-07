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
    
        def features(i):
            return dict([t for t in enumerate(self.ttm[i,:])])

        def training_example(i):
            label = "spam" if self.sm[i] else "ham"
            return (self.features(i), label)

        def sample_indices(training_ratio=TRAINING_RATIO):
            n_training = int(self.sm.size * training_ratio)
            print "Training on %s, Testing on %s" % (n_training, self.sm.size)
            print "Selecting training and testing indices"
            permuted_indices = numpy.random.permutation(self.sm.size)
            training_indices = numpy.arange(self.sm.size)[permuted_indices[n_training:]]
            testing_indices = numpy.arange(self.sm.size)[permuted_indices[:n_training]]
            return training_indices, testing_indices

        #train classifier on specified indices of the training set
        def train(training_indices,):
            # using all data for now
            print "Creating training set"
            training_set = [training_example(i) for i in training_indices]
    
            print "Training"
            classifier = nltk.NaiveBayesClassifier.train(training_set)
            return classifier

        def test(classifier, testing_indices):
            print "Creating testing set"
            testing_set = [(features(i)) for i in testing_indices]

            print "Testing"
            test_results = classifier.batch_classify(testing_set)
            print "Results are in!"
    
            accurate_test_results = [label == ('spam' if sm[testing_indices[i]] else 'ham') for i,label in enumerate(test_results)]
            return test_results, accurate_test_results

        def ratio(data):
            return float(sum(data)) / len(data)

        def compute_classifier_success(n_for_validation=N):
            ratios = []

            for n in range(N):
                train_i, test_i = self.sample_indices()
                classifier = self.train(train_i)
                results, accuracy = self.test(classifier, test_i)
                print ratio(accuracy)
                ratios.append(ratio(accuracy))
                
            mean_success = numpy.mean(ratios)

            print "Average ratio: " + str(mean_success)
            print "Spam rate: " + str(0.0 + sum(sm) / sm.size )

            return mean_success
