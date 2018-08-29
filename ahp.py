import numpy as np


class AHP(object):
    def __init__(self, data):
        self.data = data

    def start(self):
        column_sums = np.asarray(self.data).sum(axis=0).tolist()
        weights = [sum([x[y] / column_sums[y] for y in range(0, len(x))]) / len(x) for x in self.data]

        return weights
