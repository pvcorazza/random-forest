import copy
from random import randrange, randint


class Bootstrap(object):
    def __init__(self, data):
        self.attributes = data[0]
        data.pop(0)
        self.data = data
        # aproximadamente 63.2% das instâncias comporão o subconjunto de treinamento
        self.percent_instances = 0.632

    # Retorna uma partição do dataset gerado através de uma amostragem aleatória de instâncias, com reposição
    def get_partition(self):
        training_partition = []
        training_partition.append(self.attributes)
        max_index = len(self.data) - 1
        index_list = list(range(0, max_index))
        num_instances = round(max_index * self.percent_instances)
        while len(training_partition) < num_instances:
            index=randint(0, max_index)
            training_partition.append(copy.deepcopy(self.data[index]))
            if index in index_list:
                index_list.remove(index)

        test_partition = []
        test_partition.append(self.attributes)
        for i in index_list:
            test_partition.append(copy.deepcopy(self.data[i]))

        bootstrap = []
        bootstrap.append(training_partition)
        bootstrap.append(test_partition)

        return bootstrap
