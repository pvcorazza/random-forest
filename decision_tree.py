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
def get_possible_values(data, col):
    return set([row[col] for row in data])


class Node(object):
    def __init__(self):
        self.value = None
        self.childs = None


# Separa os dados em listas baseado nos atributos do index
def get_child_node_data(data, index, value):
    new_data = []
    for instance in data:
        if (instance[index] == value):
            new_data.append(instance)
    return new_data


# Verifica se todos os valores possuem a mesma classe
def is_same_class(data, index_class):
    possible_values = get_possible_values(data, index_class)
    if (len(possible_values) == 1):
        return True
    return False


def info (data, index):
    all_values = [row[index] for row in data]
    possible_values = get_possible_values(data, index)
    total_values = len(all_values)

    entropy = 0

    for val in possible_values:
        entropy=entropy-(all_values.count(val)/total_values)*math.log(all_values.count(val)/total_values,2)

    return entropy


def info_attribute(data, index, index_class):
    all_values = [row[index] for row in data]
    possible_values = get_possible_values(data, index)
    total_values = len(all_values)

    entropy = 0

    for val in possible_values:
        new_data = get_child_node_data(data, index, val)
        entropy=entropy+(len(new_data)/total_values)*info(new_data, index_class)

    return entropy

def gain(data, index_attribute, index_class):
    return info(data, index_class) - info_attribute(data, index_attribute, index_class)


def get_most_frequent_class(data, index_class):
    pass


def build_decision_tree(data, header):
    root = Node()

    # Se todos os valores possuem a mesma classe, retorna um nó folha com o valor dessa classe
    index_class = len(data[0]) - 1
    if is_same_class(data, index_class):
        root.value = data[0][index_class]
        return root

    if len(header) < 1:
        return get_most_frequent_class(data, index_class)

    # OBS.: AQUI DEVEMOS ENCONTRAR O MELHOR ATRIBUTO

    gains = []
    for attribute in header:
        index = header.index(attribute)
        gains.append(gain(data, index, index_class))

    maxIndex = gains.index(max(gains))

    value = header[maxIndex]


    index = header.index(value)
    header.pop(index)

    root.value = value
    root.childs = []

    # Encontra os possíveis valores para determinado atributo e adiciona um filho relativo a cada valor
    possible_values = get_possible_values(data, index)
    for value in possible_values:
        new_data = get_child_node_data(data, index, value)
        for x in new_data:
            del x[index]
        new_node = build_decision_tree(new_data, header)
        root.childs.append(new_node)

    return root
