import copy
from math import floor
from random import randrange

from decision_tree import Tree
from random_forest import RandomForest


class CrossValidation(object):
    def __init__(self, data):
        self.data = data

    def divide_kfolds(self, data, k):
        attributes = copy.deepcopy(data[0])
        data.pop(0)
        folds = []
        fold_size = floor(len(data) / k)
        for i in range(k):
            fold = []
            fold.append(copy.deepcopy(attributes))
            while len(fold) < fold_size:
                index = randrange(len(data))
                fold.append(data[index])
                del data[index]
            folds.append(fold)
        return folds

    def validate(self, folds, num_trees):

        attributes = folds[0][0]

        for fold in folds:
            del fold[0]

        for i in range(len(folds)):
            folds_copy = copy.deepcopy(folds)
            test = copy.deepcopy(folds_copy[i])
            del folds_copy[i]
            training = sum(folds_copy, [])
            training.insert(0, attributes)

            forest = RandomForest(copy.deepcopy(training))
            trees = forest.get_forest(num_trees)



            for instance in test:
                real_class = instance[len(instance)-1]
                del instance[len(instance)-1]
                # print(instance)
                prediction = forest.predict(trees, instance)
                print("Prediction: " + str(prediction))
                print("Real Class: " + str(real_class))


