import nltk
import numpy
import random

N = 4
TRAINING_RATIO = .9

print "Loading data from matrices"
ttm = numpy.load("tweet_topic_matrix.npy")
sm = numpy.load("spam_matrix.npy")

def features(i):
    return dict([t for t in enumerate(ttm[i,:])])

def training_example(i):
    label = "spam" if sm[i] else "ham"
    return (features(i), label)

def sample_indices():
    n_training = int(sm.size * TRAINING_RATIO)
    print "Training on %s, Testing on %s" % (n_training, sm.size)
    print "Selecting training and testing indices"
    permuted_indices = numpy.random.permutation(sm.size)
    training_indices = numpy.arange(sm.size)[permuted_indices[n_training:]]
    testing_indices = numpy.arange(sm.size)[permuted_indices[:n_training]]
    return training_indices, testing_indices

def train(training_indices):
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

ratios = []

for n in range(N):
    train_i, test_i = sample_indices()
    classifier = train(train_i)
    results, accuracy = test(classifier, test_i)
    print ratio(accuracy)
    ratios.append(ratio(accuracy))

print "Average ratio: " + str(numpy.mean(ratios))
