import copy
import csv

from bootstrap import Bootstrap
from decision_tree import Tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD-continuo.csv", "r"), delimiter=";"))

    # decision_tree = Tree(copy.deepcopy(data))
    # print(decision_tree)

    bootstrap = Bootstrap(copy.deepcopy(data))
    new_bootstrap = bootstrap.get_partition()

    bootstrap_sets = []
    for i in range(0,100):
        bootstrap_sets.append(bootstrap.get_partition())

    trees = []
    for bootstrap in bootstrap_sets:
        trees.append(Tree(copy.deepcopy(bootstrap[0])))

    instances = copy.deepcopy(data)
    instances.pop(0)

    for x in instances:
        del x[4]



    for instance in instances:
        predictions = []
        for tree in trees:
            predictions.append(tree.classify(instance, tree.root))
        predicted = max(set(predictions), key=predictions.count)
        print(predicted)



