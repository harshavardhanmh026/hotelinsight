import csv
from abc import ABC, abstractmethod

hotel_csv_params = {
        "hotel_id" : 0,
        "name" : 1,
        "state" : 2,
        "cost" : 3,
        "rating" : 4
    }

opr_list =['highest', 'cheapest', 'average']

class VerifyInput(ABC):
    @abstractmethod
    def verify(self):
        pass

class VerifyOprInput(VerifyInput):
    def verify(self, *args, **kwargs):
        val = kwargs['opr']
        if val not in opr_list:
            raise Exception(f"Not a valid Operation {val}")

class VerifyParamInput(VerifyOprInput):
    def verify(self, *args, **kwargs):
        super(VerifyParamInput, self).verify(**kwargs)
        val = kwargs['param']
        if val not in ["cost", "rating"]:
            raise Exception(f'Not a valid Parameter {val}')


class PerformOperation:
    def __init__(self, file_name, opr, param):
        with open(file_name, 'r') as csv_file:
            self.hotel_list = list(csv.reader(csv_file))[1:]
            self.total_len = len(self.hotel_list)
            self.opr = opr
            self.param = param

    def module_nav(self):
        if self.opr == opr_list[0]:
            return self.highest
        elif self.opr == opr_list[1]:
            return self.cheapest
        else:
            return self.average

    def highest(self, state):
        state_idx = hotel_csv_params["state"]
        param_idx = hotel_csv_params[self.param]

        val = [0, 0, 0, 0, 0]

        for index in range(self.total_len//2):
            val = max(self.hotel_list[index] if self.hotel_list[index][state_idx].lower() == state else val,
                val,
                self.hotel_list[self.total_len-index-1] if self.hotel_list[self.total_len-index-1][state_idx].lower() == state else val,
                key=lambda x : float(x[param_idx]))
        return val

    def cheapest(self, state):
        state_idx = hotel_csv_params["state"]
        param_idx = hotel_csv_params[self.param]

        val = [0, 0, 0, 0, 0]
        val[param_idx] = float('inf')

        for index in range(self.total_len//2):
            val = min(self.hotel_list[index] if self.hotel_list[index][state_idx].lower() == state else val,
                val,
                self.hotel_list[self.total_len-index-1] if self.hotel_list[self.total_len-index-1][state_idx].lower() == state else val,
                key=lambda x : float(x[param_idx]))
        return val

    def average(self, state):
        state_idx = hotel_csv_params["state"]
        param_idx = hotel_csv_params[self.param]

        val = 0.0

        for index in range(self.total_len//2):
            val += float(self.hotel_list[index][param_idx]) if self.hotel_list[index][state_idx].lower() == state else 0.0
            val += float(self.hotel_list[self.total_len-index-1][param_idx]) if self.hotel_list[self.total_len-index-1][state_idx].lower() == state else 0.0
        val /= self.total_len
        return [val, state]

    def output_formatter(self, val):
        if self.opr == opr_list[0]:
            param_idx = hotel_csv_params[self.param]
            identifier =  'price' if self.param == 'cost' else 'rating'
            print(f'Hotel with highest {identifier} in {val[2]} is {val[1]} with {param} {val[param_idx]}')
        elif self.opr == opr_list[1]:
            param_idx = hotel_csv_params[self.param]
            identifier =  'price' if self.param == 'cost' else 'rating'
            print(f'Hotel with cheapest {identifier} in {val[2]} is {val[1]} with {param} {val[param_idx]}')
        else:
            print(f'Average rating of Hotel in {val[1]} is {val[0]}')


if __name__ == '__main__':
    state = input("What is the state : ").lower()
    param = input("Cost or Rating : ").lower()
    opr = input("Operation : ").lower()

    verifier = VerifyParamInput()
    verifier.verify(opr=opr, param=param)

    performer = PerformOperation('hotels.csv', opr, param)
    value = performer.module_nav()(state)
    performer.output_formatter(value)
