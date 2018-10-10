import copy

from bootstrap import Bootstrap
from decision_tree import Tree


class RandomForest(object):
    def __init__(self, data):
        self.data = data

    def get_forest(self, size):
        bootstrap = Bootstrap(copy.deepcopy(self.data))

        bootstrap_sets = []
        for i in range(0, size):
            bootstrap_sets.append(bootstrap.get_partition())

        trees = []
        for bootstrap in bootstrap_sets:
            trees.append(Tree(copy.deepcopy(bootstrap[0]), True))

        return trees

    def predict(self, trees, instance):

        predictions = []
        for tree in trees:
            predictions.append(tree.classify(instance, tree.root))
        predicted = max(set(predictions), key=predictions.count)

        return predicted