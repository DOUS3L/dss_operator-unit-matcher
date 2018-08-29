import numpy as np
import pandas as pd
from ahp import AHP
from topsis import Topsis
from modified_rothperanson import Matcher


class MatchingOPTYPE(object):
    def __init__(self, ahp_data, topsis_data):
        self.ahp_data = ahp_data
        self.topsis_data = topsis_data

    def run(self):
        criteria_weights = self.start_ahp(self.ahp_data)
        self.topsis_res = self.start_topsis(criteria_weights, self.topsis_data)
        self.hasilmatch = self.start_matching(np.asarray(self.topsis_res))

        self.operator_unit = {}
        unique_operators = np.unique(np.asarray(self.topsis_res)[:, 0]).tolist()

        for operator in unique_operators:
            temp = {}
            for y in self.topsis_res:
                if y[0] == operator:
                    temp[y[1]] = y[2]
            self.operator_unit[operator] = temp

    def start_ahp(self, data):
        ahp = AHP(data)
        return ahp.start()

    def start_topsis(self, criteria_weights, data):
        typeids = np.unique(data[:, :1])
        type_result = []
        for typeid in typeids:
            current_data = data[np.where(data[:, 0] == typeid)][:, 1:]
            topsis = Topsis(criteria_weights, current_data)
            topsis_result = topsis.run()

            for x in topsis_result:
                type_result.append([x[0], typeid, x[1]])

        return type_result

    def start_matching(self, data):
        # data = np.asarray(data)
        operators = np.unique(np.asarray(data)[:, 0]).tolist()
        operator_data = []
        for x in operators:
            temp = []
            for y in range(0, len(data)):
                if x == data[y, 0]:
                    temp.append([data[y, 1], data[y, 2]])
            operator_data.append([x, temp])
        # print(operator_data)
        unit_data = pd.read_csv('static/Unit Data.csv').values.tolist()  # nanti diganti
        # unit_data = [['ABC101', 3], ['ABC102', 4]]  # hardcode
        match = Matcher(operator_data, unit_data)
        match.start_assign()
        final_match = match.results()

        return final_match
