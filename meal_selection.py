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
        # Get data about user AHP preferences
        query_ahp_pref = f"SELECT users.name, ahp_pref_name, value FROM users INNER JOIN user_ahp_pref ON users.id=user_ahp_pref.user_id WHERE users.name {query_filter}"
        result_ahp_pref = pd.read_sql_query(query_ahp_pref, self.database).set_index(['name', 'ahp_pref_name'])
        # Get data about user other preferences
        query_pref = f"SELECT users.name, type_name, subtype, value FROM users INNER JOIN user_pref ON users.id=user_pref.user_id WHERE users.name {query_filter}"
        result_pref = pd.read_sql_query(query_pref, self.database).set_index(['name', 'type_name', 'subtype'])
        result_pref = result_pref.sort_index()
        # Calculate meal rating for each user
        self.meals['Rating'] = 0
        user_ratings = []
        for user in self.users:
            user_raw_preferences = result_ahp_pref.loc[user, 'typ-kuchnia']['value'], result_ahp_pref.loc[user, 'kuchnia-smak']['value'], result_ahp_pref.loc[user, 'typ-smak']['value']
            user_AHP = AHP(*user_raw_preferences)
            user_preferences = user_AHP.get_preferences() # [typ, kuchnia, smak]
            # Prepare Data Frame for user rating calculations
            user_meals_rating = self.meals.loc[:, ('name', 'Rating')].copy()
            user_meals_rating['type_rating'] = 0
            user_meals_rating['kitchen_rating'] = 0
            user_meals_rating['taste_rating'] = 0
            # Calculate score for meal taste
            tastes_list = list(result_pref.loc[user, 'smak'].index)
            for taste in tastes_list:
                user_meals_rating['taste_rating'] += self.meals[taste] * result_pref.loc[user, 'smak', taste].value
            # Calculate score for meal type
            types_list = list(result_pref.loc[user, 'typ'].index)
            for type_ in types_list:
                user_meals_rating['type_rating'] += self.meals[type_] * result_pref.loc[user, 'typ', type_].value
            # Calculate score for meal kitchen
            kitchens_list = list(result_pref.loc[user, 'kuchnia'].index)
            for kitchen in kitchens_list:
                user_meals_rating['kitchen_rating'] += self.meals[kitchen] * result_pref.loc[user, 'kuchnia', kitchen].value
            # Sum scores
            for i, rating in zip(range(0, 3), ['type_rating', 'kitchen_rating', 'taste_rating']):
                user_meals_rating['Rating'] += user_meals_rating[rating] * user_preferences[i]
            user_ratings.append(user_meals_rating)
        weight_sum = 0
        for weight, rating in zip(self.weights, user_ratings):
            weight_sum += weight
            self.meals['Rating'] += rating['Rating'] * weight
        self.meals['Rating'] = self.meals['Rating'] / weight_sum
        self.meals_rated = self.meals.loc[:, ('name', 'Rating')].sort_values(by='Rating', ascending=False)
        return self.meals_rated