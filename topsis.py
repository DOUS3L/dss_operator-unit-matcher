import numpy as np


class Topsis(object):
    def __init__(self, cweight, data):
        self.data = data[:, 1:].astype(np.float)
        self.operators = np.squeeze(data[:, :1]).tolist()
        # self.alternative = x.shape[0]
        # self.criteria = x.shape[1]
        if len(cweight) != self.data.shape[1]:
            raise Exception('Criteria weight is not valid.')
        else:
            self.cweight = np.asarray(cweight)

    def run(self):
        self.normalize()
        self.mcweight()
        self.getdistance()
        self.calculatefinal()

        return self.range

    def normalize(self):
        self.normalized = []
        norm = [np.linalg.norm(x) for x in self.data.transpose()]

        for x in self.data:
            temp = []
            for y in range(0, self.data.shape[1]):
                temp.append(x[y] / norm[y])
            self.normalized.append(temp)
        self.normalized = np.asarray(self.normalized)

    def mcweight(self):
        self.multipliedw = []

        for x in self.normalized:
            self.multipliedw.append(x * self.cweight)
        self.multipliedw = np.asarray(self.multipliedw)

    def getdistance(self):
        self.distance = []
        self.positives = []
        self.negatives = []
        for x in self.multipliedw.transpose():
            self.positives.append(np.max(x))
            self.negatives.append(np.min(x))

        self.positives = np.asarray(self.positives)
        self.negatives = np.asarray(self.negatives)

        self.pdistance = []
        self.ndistance = []
        for x in self.multipliedw:
            self.pdistance.append(np.sqrt(sum((self.positives - x)**2)))
            self.ndistance.append(np.sqrt(sum((self.negatives - x)**2)))

    def calculatefinal(self):
        self.range = []

        for x in range(0, self.data.shape[0]):
            self.range.append([self.operators[x], 1 - (self.ndistance[x] / (self.ndistance[x] + self.pdistance[x]))])

        self.range.sort(key=lambda x: x[1], reverse=True)
