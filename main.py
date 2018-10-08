import csv

from decision_tree import Tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD.csv", "r"), delimiter=";"))


    decision_tree = Tree(data)

    print(decision_tree)


