import numpy as np

class AHP:
    def __init__(self, *sliders):
        """
        Handles whole AHP weights and stuff
        Input: Sliders values
        """
        # Prepare matrix
        self.criteria_count = len(sliders)
        self.matrix = self._prepare_matrix(sliders)
        self.normalized_matrix = self._normalize_matrix()
        self.global_preferences = self._calculate_preferences()

    def _prepare_matrix(self, criteria):
        """
        Input: 1D iterable with n numbers
        Output: matrix nxn
        """
        matrix = np.empty(shape=(self.criteria_count, self.criteria_count))
        for _i in range(self.criteria_count):
            value = criteria[_i]

            # Adjust values from sliders, 0 is 1
            if value == 0:
                value = 1
            # If negative then change to positive and invert eg. -3 -> 1/3
            elif value < 0:
                value = self._inv(-value)

            # Insert 1 on matrix diagonal
            matrix[_i, _i] = 1
            # Fill according to Uji = 1/Uij
            _j = _i + 1 if (_i + 1 < self.criteria_count) else 0
            if _j == 0:
                value = self._inv(value)
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

    def _calculate_preferences(self, matrix=None):
        """Calculate global preferences weights for all criteria"""
        if matrix is None:
            matrix = self.normalized_matrix
        return np.sum(matrix, axis=1)/self.criteria_count

    def _inv(self, value):
        """Inverts number eg. 9 to 1/9"""
        return 1 / value

AHP(3, 5, 9)
# Creates this matrix:
# [[1.         3.         9.        ]
#  [0.33333333 1.         5.        ]
#  [0.11111111 0.2        1.        ]]