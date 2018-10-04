import math

def entropy(matrixInstances):
    totalInstances = matrixInstances.__len__()
    featuresEntropy = []
    for feature in range(matrixInstances[0].__len__()):
        values = {}
        for instance in range(matrixInstances.__len__()):
            currentFeatureValue = matrixInstances[instance][feature]
            if(currentFeatureValue in values):
                oldValue = values[currentFeatureValue]
                oldValue.append(instance)
                values[currentFeatureValue] = oldValue
            else:
                list = []
                list.append(instance)
                values[currentFeatureValue] = list
        entropy = 0
        print (values)
        for currentFeatureValue in values.keys():
            labels = {}
            setSize = values[currentFeatureValue].__len__()
            currentEntropy = 0
            for instance in values[currentFeatureValue]:
                label = matrixInstances[instance][(len(matrixInstances[0])-1)]
                if(label in labels):
                    oldValue = labels[label]
                    newValue = oldValue + 1
                    labels[label] = newValue
                else:
                    labels[label] = 1
            for label in labels.keys():
                currentEntropy = currentEntropy - round(((labels[label])/setSize)*math.log((labels[label])/setSize, 2),3)
            currentEntropy = currentEntropy * (setSize/totalInstances)
            entropy = entropy + currentEntropy
        featuresEntropy.append(entropy)
    print (featuresEntropy)
    exit(0)



matrixInstances = None
with open("dadosBenchmark_validacaoAlgoritmoAD.csv") as instances:
    for instance in instances:
        splittedInstance = instance.split(';')
        if(matrixInstances != None):
            currentInstance = []
            for field in splittedInstance:
                currentInstance.append(field)
            matrixInstances.append(currentInstance)
        else:
            matrixInstances = []
featuresEntropy = entropy(matrixInstances)