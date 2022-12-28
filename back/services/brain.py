import nltk

class Brain:
    def __init__(self) -> None:
        pass
    def split_dataset(self, dataset:list, dataset_count:int=1900) -> dict:
        training_set = dataset[:dataset_count]
        testing_set = dataset[dataset_count:]
        
        return training_set, testing_set
    
    def train(self, dataset) -> nltk.NaiveBayesClassifier:
        training_set, testing_set = self.split_dataset(dataset)
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print("Classifier accuracy :",(nltk.classify.accuracy(classifier, testing_set))*100)
        classifier.show_most_informative_features(15)
        
        return classifier