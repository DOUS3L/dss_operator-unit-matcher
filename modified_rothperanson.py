import numpy as np


class Operator():

    def __init__(self, id, units, unit_score):
        self.id = id
        self.unit_score = unit_score
        self.units = units
        self.assigned = False
        self.unit = None

    def assign(self, unit, score):
        self.assigned = True
        self.unit = unit
        self.assigned_score = score
        # print(self.id + ' assigned to ' + self.unit)

    def resign(self):
        # print(self.id + ' kicked from ' + self.unit)
        self.assigned = False
        self.unit = None

    def next_unit(self):
        return self.units.pop(), self.unit_score.pop()

    def try_assign(self):
        try:
            self.current_unit, self.current_score = self.next_unit()
        except IndexError:
            return False

        if self.current_unit.assign(self):
            return True

        self.try_assign()


class Type():

    def __init__(self, id, total_assign):
        self.id = id
        self.assigned_operators = []
        self.total_assign = total_assign

    def add(self, operator):
        self.assigned_operators.append(operator)
        self.assigned_operators.sort(key=lambda x: x.current_score[1], reverse=True)
        operator.assign(self.id, operator.current_score)
        # print('Tipe ' + self.id + ' berisi ' + str(len(self.assigned_operators)))

    def assign(self, operator):
        if len(self.assigned_operators) < self.total_assign:
            # print(operator.id + ' Assign1')
            self.add(operator)

            return True
        if self.assigned_operators[-1].current_score[1] < operator.current_score[1]:
            # print(operator.id + 'Assign2')
            replaced = self.assigned_operators.pop()
            replaced.resign()
            self.add(operator)
            replaced.try_assign()
            return True

        return False


class Matcher():
    def __init__(self, operator_data, unit_data):
        # unit_data taken as pandas dataframes
        self.operator_data = operator_data
        self.unit_data = unit_data

        self.units = {}
        self.operators = {}

        for x in self.unit_data:
            self.units[x[0]] = Type(x[0], x[1])

        for x in self.operator_data:
            units = sorted(x[1], key=lambda i: i[1])
            unit_objects = [self.units[y[0]] for y in units]
            self.operators[x[0]] = Operator(x[0], unit_objects, units)

    def start_assign(self):
        for k, v in self.operators.items():
            v.try_assign()

    def results(self):
        results = {}

        for k, v in self.units.items():
            temp = {}
            for operator in v.assigned_operators:
                temp[operator.id] = operator.assigned_score[1]
            results[k] = temp

        # for k, v in self.operators.items():
        #     try:
        #         results[k] = v.unit
        #     except AttributeError:
        #         results[k] = 'No match'

        # for k, v in self.units.items():
        #     try:
        #         results[k] = v.assigned_operators
        #     except AttributeError:
        #         results[k] = 'No match'

        return results
