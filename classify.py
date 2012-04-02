import nltk
import numpy
import random

TRAINING_RATIO = .9

print "Loading data from matrices"
ttm = numpy.load("tweet_topic_matrix.npy")
sm = numpy.load("spam_matrix.npy")

def features(i):
    return dict([t for t in enumerate(ttm[i,:])])

def training_example(i):
    label = "spam" if sm[i] else "ham"
    return (features(i), label)

n_training = int(sm.size * TRAINING_RATIO)
print "Training on %s, Testing on %s" % (n_training, sm.size)
print "Selecting training and testing indices"
permuted_indices = numpy.random.permutation(sm.size)
testing_indices = numpy.arange(sm.size)[permuted_indices[:n_training]]
training_indices = numpy.arange(sm.size)[permuted_indices[n_training:]]

# using all data for now
print "Creating training set"
training_set = [training_example(i) for i in training_indices]

print "Creating testing set"
testing_set = [(features(i)) for i in testing_indices]

print "Training"
classifier = nltk.NaiveBayesClassifier.train(training_set)

print "Testing"
test_results = classifier.batch_classify(testing_set)

print "Results are in!"

accurate_test_results = [label == ('spam' if sm[testing_indices[i]] else 'ham') for i,label in enumerate(test_results)]

print "Accuracy rate:"
print float(sum(accurate_test_results)) / len(accurate_test_results)

print "Spam Rate:"
print float(sum(sm[testing_indices])) / len(testing_indices)
