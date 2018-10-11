import copy
import csv

from bootstrap import Bootstrap
from cross_validation import CrossValidation
from decision_tree import Tree
from random_forest import RandomForest


def read_data(filename):
    if filename == "benchmark.csv" or filename == "benchmark-continuo.csv":
        data = list(csv.reader(open("data/" + filename, "r"), delimiter=";"))
        return data

    data = list(csv.reader(open("data/" + filename, "r"), delimiter=","))
    if not data:
        return None

    # Breast Cancer Wisconsin (32 atributos, 569 exemplos, 2 classes)
    # https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)
    # Objetivo: predizer se um determinado exame médico indica ou não a presença de câncer.
    if filename == "wdbc.data":

        # 1) ID number
        # 2) Diagnosis (M = malignant, B = benign)
        # 3-32)
        #
        # Ten real-valued features are computed for each cell nucleus:
        #
        # 	a) radius (mean of distances from center to points on the perimeter)
        # 	b) texture (standard deviation of gray-scale values)
        # 	c) perimeter
        # 	d) area
        # 	e) smoothness (local variation in radius lengths)
        # 	f) compactness (perimeter^2 / area - 1.0)
        # 	g) concavity (severity of concave portions of the contour)
        # 	h) concave points (number of concave portions of the contour)
        # 	i) symmetry
        # 	j) fractal dimension ("coastline approximation" - 1)
        attributes = ['Id', 'Diagnosis', 'RadiusMean', 'TextureMean', 'PerimeterMean', 'AreaMean', 'SmoothnessMean',
                      'CompactnessMean', 'ConcavityMean', 'ConcavePointsMean', 'SymmetryMean', 'FractalDimensionMean',
                      'RadiusSE', 'TextureSE', 'PerimeterSE', 'AreaSE', 'SmoothnessSE',
                      'CompactnessSE', 'ConcavitySE', 'ConcavePointsSE', 'SymmetrySE', 'FractalDimensionSE',
                      'RadiusWorst', 'TextureWorst', 'PerimeterWorst', 'AreaWorst', 'SmoothnessWorst',
                      'CompactnessWorst', 'ConcavityWorst', 'ConcavePointsWorst', 'SymmetryWorst',
                      'FractalDimensionWorst',
                      ]

        data.insert(0, attributes)

        # Remove os valores para o ID
        for x in data:
            del x[0]

        # Posiciona a classe ao final dos dados para padronização
        for x in data:
            x.append(copy.deepcopy(x[0]))
            del x[0]

        return data

    # Wine Data Set (13 atributos, 178 exemplos, 3 classes)
    # https://archive.ics.uci.edu/ml/datasets/wine
    # Objetivo: predizer o tipo de um vinho baseado em sua composição química
    if filename == "wine.data":

        attributes = ['Class', 'Alcohol', 'Malic', 'Ash', 'Alcalinity', 'Magnesium', 'Phenols',
                      'Flavanoids', 'Nonflavanoid', 'Proanthocyanins', 'Color', 'Hue', 'Od', 'Proline']

        data_formatted = []
        for l in data:
            data_formatted.append([str(float(i)) for i in l])

        data.insert(0, attributes)

        # Posiciona a classe ao final dos dados para padronização
        for x in data:
            x.append(copy.deepcopy(x[0]))
            del x[0]

        return data_formatted

    # 3. Ionosphere Data Set (34 atributos, 351 exemplos, 2 classes)
    # https://archive.ics.uci.edu/ml/datasets/Ionosphere
    # Objetivo: predizer se a captura de sinais de um radar da ionosfera é adequada para
    # análises posteriores ou não (’good’ ou ’bad’)
    if filename == "ionosphere.data":

        attributes = []

        for i in range(34):
            attributes.append("Signal" + str(i))

        attributes.append("Class")

        data.insert(0, attributes)

        return data


if __name__ == '__main__':
    data = read_data("wine.data")

    cross_validation = CrossValidation(copy.deepcopy(data))
    folds = cross_validation.divide_kfolds(copy.deepcopy(data), 10)
    cross_validation.validate(folds,10)
    exit()

    forest = RandomForest(copy.deepcopy(data))

    trees = forest.get_forest(100)

    instance = ["Ensolarado", "Amena", "Alta", "Falso"]

    prediction = forest.predict(trees, instance)

    print(prediction)
