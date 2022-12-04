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