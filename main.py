import csv

from decision_tree import Tree

if __name__ == '__main__':
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD.csv", "r"), delimiter=";"))

    decision_tree = Tree(data)
    instance = ["Ensolarado","Amena","Alta","Verdadeiro"]
    predicted_class = decision_tree.classify(instance, decision_tree.root)
    print(predicted_class)