import pandas as pd
import numpy as np
from ahp import AHP


class MealSelection:
    def __init__(self, database, users_and_weights):
        self.database = database.connect
        self.users, self.weights = self._extract_users_and_weights(users_and_weights)
        self.meat, self.allergens = self._get_all_restrictions()
        self.meals = self._get_all_meals()
        self.meals = self._apply_allergen_restrictions()

    def _extract_users_and_weights(self, users_and_weights):
        """Extracts data from [(usercombo, weightfield), ...]"""
        users = []
        weights = []
        for user, weight in users_and_weights:
            users.append(user.get())
            weights.append(float(weight.get()))
        return tuple(users), tuple(weights)

    def _get_all_meals(self):
        """Retrieves all meals from database"""
        query = "SELECT * FROM meals"
        return pd.read_sql_query(query, self.database).set_index(['id'])

    def _get_all_restrictions(self):
        """Retrieves informations about all possible restrictions for selected users"""
        # If only one user is given then query must be altered a bit, otherwise it will throw an error
        query_filter = f"IN {self.users}" if len(self.users) > 1 else f"= '{self.users[0]}'"
        query = f"SELECT res_name, SUM(value) FROM users INNER JOIN user_res ON users.id=user_res.user_id WHERE users.name {query_filter} GROUP BY res_name"
        result = pd.read_sql_query(query, self.database).set_index(['res_name'])
        meat_data = result.loc[['ryby', 'weganin', 'wegetarianin']]
        allergens_data = result.loc[result.index.difference(meat_data.index).values]
        return meat_data, allergens_data

    def _apply_allergen_restrictions(self):
        """Filters out allergenic meals"""
        active_allergens = self.allergens.loc[self.allergens['SUM(value)'] >= 1].index.values
        filtered_meals = self.meals
        for allergen in active_allergens:
            filtered_meals = filtered_meals.loc[filtered_meals[allergen] < 1]
        return filtered_meals