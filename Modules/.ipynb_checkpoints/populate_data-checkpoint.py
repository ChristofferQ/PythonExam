def populate_price():
    """
    Run this to populate ingredients_prices.csv with random integers for each ingredient
    """
    import pandas as pd
    import random

    df1 = pd.read_csv('./Data/ingredients_prices.csv')

    Ingredient = df1['Ingredient']
    Price = []

    for item in Ingredient:
        Price.append(random.randint(5, 110))

    df2 = pd.DataFrame(list(zip(*[Ingredient, Price])), columns = ['Ingredient','Price'])
    df2.to_csv('./Data/ingredients_prices.csv', index=False)
    
def populate_nourishment():
    """
    Run this to populate ingredients_nourishment.csv with random integers for each ingredient
    """
    import pandas as pd
    import random

    df1 = pd.read_csv('./Data/ingredients_nourishment.csv')

    Ingredient = df1['Ingredient']
    Kcal = []

    for item in Ingredient:
        Kcal.append(random.randint(5, 110))

    df2 = pd.DataFrame(list(zip(*[Ingredient, Kcal])), columns = ['Ingredient','Kcal'])
    df2.to_csv('./Data/ingredients_nourishment.csv', index=False)
    
def populate_missing_ingredients():
    """
    This function checks to see if ingredients are missing from ingredients_prices.csv and ingredients_nourishment.csv. It will then add and populate them. 
    """
    from Modules.populate_data import populate_price, populate_nourishment
    import pandas as pd
    import csv

    df1 = pd.read_csv('./Data/recipe_ingredients.csv')
    df2 = pd.read_csv('./Data/ingredients_prices.csv')

    recipe_ingredients = []
    existing_ingredients = []

    for item in df1["Ingredient"]:
        recipe_ingredients.append(item)

    for item in df2["Ingredient"]:
        existing_ingredients.append(item)

    remaining_ingredients = list(set(recipe_ingredients) - set(existing_ingredients))

    for item in remaining_ingredients:
        with open('./Data/ingredients_prices.csv', 'a') as fd:
            fd.write(item + "," + '\n')

    for item in remaining_ingredients:
        with open('./Data/ingredients_nourishment.csv', 'a') as fd:
            fd.write(item + "," + '\n')

    populate_price()
    populate_nourishment()