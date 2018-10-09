import copy
import csv

from bootstrap import Bootstrap
from decision_tree import Tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD-continuo.csv", "r"), delimiter=";"))

    decision_tree = Tree(copy.deepcopy(data))

    bootstrap = Bootstrap(data)
    print(bootstrap.sub_partition(0.8))