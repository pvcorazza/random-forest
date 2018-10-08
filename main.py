import csv

import decision_tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD.csv", "r"), delimiter=";"))
    header = data[0]
    data.pop(0)
    root = decision_tree.build_decision_tree(data, header)

    print (root)

