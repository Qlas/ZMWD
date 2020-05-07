import numpy as np

class AHP:
    def __init__(self, sliders):
        # Prepare matrix
        self.matrix = self._prepare_matrix(sliders)
        self.normalized_matrix = self._normalize_matrix(self.matrix)

    def _prepare_matrix(self, criteria):
        """
        Input: 1D iterable with n numbers
        Output: matrix nxn
        """
        _criteria_count = len(criteria)
        matrix = np.empty(shape=(_criteria_count, _criteria_count))
        for _i in range(_criteria_count):
            value = criteria[_i]
            if value == 0:
                value = 1
            elif value < 0:
                value = self._inv(-value)
            matrix[_i, _i] = 1
            _j = _i + 1 if (_i + 1 < _criteria_count) else 0
            matrix[_i, _j] = value
            matrix[_j, _i] = self._inv(value)
        return matrix

    def _normalize_matrix(self, matrix=None):
        """Normalize matrix columns to 1"""
        if matrix is None:
            matrix = self.matrix
        column_sum = np.sum(matrix, axis=0)
        normalized_matrix = matrix/column_sum
        return normalized_matrix

    def _inv(self, value):
        """Inverts number eg. 9 to 1/9"""
        return 1 / value

AHP((3, 5, 9))
# Creates this matrix:
# [[1.         3.         0.11111111]
#  [0.33333333 1.         5.        ]
#  [9.         0.2        1.        ]]