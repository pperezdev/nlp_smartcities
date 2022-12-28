import nltk
import pickle

featuresets = []

dataset_count = 1900

training_set = featuresets[:dataset_count]
testing_set = featuresets[dataset_count:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Classifier accuracy :",(nltk.classify.accuracy(classifier, testing_set))*100)

classifier.show_most_informative_features(15)