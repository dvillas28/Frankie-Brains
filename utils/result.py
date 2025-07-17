# result.py

class Result():
    def __init__(self, valid: bool, data=None, result_type=None):
        self.valid = valid
        self.data = data
        self.result_type = result_type
