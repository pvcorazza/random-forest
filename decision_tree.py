import csv
import math


def entropy(matrixInstances):
    totalInstances = matrixInstances.__len__()
    featuresEntropy = []
    for feature in range(matrixInstances[0].__len__()):
        values = {}
        for instance in range(matrixInstances.__len__()):
            currentFeatureValue = matrixInstances[instance][feature]
            if (currentFeatureValue in values):
                oldValue = values[currentFeatureValue]
                oldValue.append(instance)
                values[currentFeatureValue] = oldValue
            else:
                list = []
                list.append(instance)
                values[currentFeatureValue] = list
        entropy = 0
        print(values)
        for currentFeatureValue in values.keys():
            labels = {}
            setSize = values[currentFeatureValue].__len__()
            currentEntropy = 0
            for instance in values[currentFeatureValue]:
                label = matrixInstances[instance][(len(matrixInstances[0]) - 1)]
                if (label in labels):
                    oldValue = labels[label]
                    newValue = oldValue + 1
                    labels[label] = newValue
                else:
                    labels[label] = 1
            for label in labels.keys():
                currentEntropy = currentEntropy - round(
                    ((labels[label]) / setSize) * math.log((labels[label]) / setSize, 2), 3)
            currentEntropy = currentEntropy * (setSize / totalInstances)
            entropy = entropy + currentEntropy
        featuresEntropy.append(entropy)
    print("\n")
    print(featuresEntropy)
    exit(0)


# Possíveis valores para a coluna
def get_possible_values(rows, col):
    return set([row[col] for row in rows])


class Node(object):
    def __init__(self):
        self.value = None
        self.next = None
        self.childs = None
        self.data = None


# Separa os dados em listas baseado nos atributos do index
def get_child_node(root, index, value):
    new_node = Node()
    new_node.value = value
    new_data = []
    for instance in root.data:
        if (instance[index] == value):
            new_data.append(instance)
    new_node.data = new_data
    return new_node


# Verifica se todos os valores possuem a mesma classe
def is_same_class(data, index_class):
    possible_values = get_possible_values(data, index_class)
    if (len(possible_values) == 1):
        return True
    return False


def build_decision_tree(data, header):
    root = Node()


    # Se todos os valores possuem a mesma classe, retorna um nó folha com o valor dessa classe
    index_class = header.index("Joga")
    if is_same_class(data, index_class):
        root.value = data[0][index_class]
        return root

    # OBS.: AQUI DEVEMOS ENCONTRAR O MELHOR ATRIBUTO

    index = header.index("Tempo")

    # print(data)

    root.data = data
    root.value = "Tempo"
    root.childs = []

    # Encontra os possíveis valores para determinado atributo e adiciona um filho relativo a cada valor
    possible_values = get_possible_values(root.data, index)
    for value in possible_values:
        new_node = get_child_node(root, index, value)
        root.childs.append(new_node)

    for c in root.childs:
        print(c.data)
