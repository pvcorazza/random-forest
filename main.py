import csv

from decision_tree import Tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD-continuo.csv", "r"), delimiter=";"))

    decision_tree = Tree(data)

    for x in data:
        del x[4]

    for instance in data:
        predicted_class = decision_tree.classify(instance, decision_tree.root)
        print(predicted_class)