import csv

from decision_tree import Tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD2.csv", "r"), delimiter=";"))


    decision_tree = Tree(data)
    print(decision_tree)
    decision_tree.printTree()


