import pandas as pd
import numpy as np
from ahp import AHP


class MealSelection:
    def __init__(self, database, users_and_weights, meal_type):
        self.database = database.connect
        self.users = tuple([row[0] for row in users_and_weights])
        self.weights = tuple([row[1] for row in users_and_weights])
        self.users_count = len(self.users)
        self.meat, self.allergens = self._get_all_restrictions()
        self.meals = self._get_all_meals()
        self.meals = self._apply_meal_restriction(meal_type)
        self.meals = self._apply_allergen_restrictions()
        self.meals = self._apply_meat_restrictions()
        self.rate_meals()

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
        meat_data = result.loc[['mięso', 'ryby', 'weganin', 'wegetarianin']]
        allergens_data = result.loc[result.index.difference(meat_data.index).values]
        return meat_data, allergens_data

    def _apply_allergen_restrictions(self):
        """Filters out allergenic meals"""
        active_allergens = self.allergens.loc[self.allergens['SUM(value)'] >= 1].index.values
        filtered_meals = self.meals
        for allergen in active_allergens:
            filtered_meals = filtered_meals.loc[filtered_meals[allergen] < 1]
        return filtered_meals

    def _apply_meal_restriction(self, meal_type):
        """Filters out all meal types except the one given"""
        return self.meals.loc[self.meals[meal_type] >= 1]

    def _apply_meat_restrictions(self):
        """Filters out meaty meals if needed"""
        # Filter out fish if not everyone eats them
        filtered_meals = self.meals
        if (float(self.meat.loc['ryby']) <= self.users_count):
            filtered_meals = filtered_meals.loc[filtered_meals['ryby'] < 1]
        # Now filter out regular meat if any vege type is active
        for vege_type in ['wegetarianin', 'weganin']:
            if (float(self.meat.loc[vege_type]) >= 1):
                filtered_meals = filtered_meals.loc[filtered_meals[vege_type] >= 1]
        return filtered_meals

    def rate_meals(self):
        """Handles meal rating procedure"""
        # If only one user is given then query must be altered a bit, otherwise it will throw an error
        query_filter = f"IN {self.users}" if len(self.users) > 1 else f"= '{self.users[0]}'"
        # Get data about user preferences
        query = f"SELECT users.name, ahp_pref_name, value FROM users INNER JOIN user_ahp_pref ON users.id=user_ahp_pref.user_id WHERE users.name {query_filter}"
        result = pd.read_sql_query(query, self.database).set_index(['name'])
        # Calculate meal rating for each user
        for user in self.users:
            user_raw_preferences = list(result.loc[user]['value'])
            user_AHP = AHP(*user_raw_preferences)
            user_preferences = user_AHP.get_preferences()