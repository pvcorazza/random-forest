from random import randrange


class Bootstrap(object):
    def __init__(self, data):
        data.pop(0)
        self.data = data

    def sub_partition(self, ratio):
        sample = list()
        n_sample = round(len(self.data) * ratio)
        while len(sample) < n_sample:
            index = randrange(len(self.data))
            sample.append(self.data[index])
        return sample