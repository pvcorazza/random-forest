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


def create_decision_tree(data):
    node = {"att": None, "value": {}}
    # if (data.values())


def calculate():
    data = list(csv.reader(open("data/dadosBenchmark_validacaoAlgoritmoAD.csv", "r"), delimiter=";"))
    header = data[0]
    index = header.index("Tempo")
    data.pop(0)
    # print(data)

    
    # Separa os dados em listas baseado nos atributos do index
    possible_values = get_possible_values(data, index)
    for value in possible_values:
        new_data = []
        for instance in data:
            if (instance[index] == value):
                new_data.append(instance)
        print(new_data)
