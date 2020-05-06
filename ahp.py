import numpy as np

class AHP:
    def __init__(self, sliders):
        # Prepare matrix
        _sliders_count = len(sliders)
        self.matrix = np.empty(shape=(_sliders_count, _sliders_count))
        for _i in range(_sliders_count):
            value = sliders[_i]
            if value == 0:
                value = 1
            elif value < 0:
                value = self._inv(-value)
            self.matrix[_i, _i] = 1
            _j = _i + 1 if (_i + 1 < _sliders_count) else 0
            self.matrix[_i, _j] = value
            self.matrix[_j, _i] = self._inv(value)

    def _inv(self, value):
        """Inverts number eg. 9 to 1/9"""
        return 1 / value

AHP((3, 5, 9))
# Creates this matrix:
# [[1.         3.         0.11111111]
#  [0.33333333 1.         5.        ]
#  [9.         0.2        1.        ]]