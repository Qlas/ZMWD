import pandas as pd
import numpy as np
from ahp import AHP


class MealSelection:
    def __init__(self, database, users_and_weights):
        self.database = database
        self.users, self.weights = self._extract_users_and_weights(users_and_weights)

    def _extract_users_and_weights(self, users_and_weights):
        users = []
        weights = []
        for user, weight in users_and_weights:
            users.append(user.get())
            weights.append(float(weight.get()))
        return tuple(users), tuple(weights)
