def merge_price(csv_file):
    """
    This function merges the given file with ingredients_prices.csv and returns the result.
    """
    import pandas as pd
    
    df1 = pd.read_csv('./Data/ingredients_prices.csv')
    df2 = pd.read_csv('./Data/' + csv_file + '.csv')
    
    result = pd.merge(df1,df2)
    
    return result

def get_price_of_ingredients(csv_file):
    """
    This function uses merge_price() to get ingredients individual price and show_price_of_ingredients() to display the result.
    """
    import pandas as pd

    result = merge_price(csv_file)
    show_price_of_ingredients(result)

def show_price_of_ingredients(data):
    """
    This function displays the data from the given dataset by printing it and displaying it in a bar chart.
    """
    import pandas as pd 
    import matplotlib.pyplot as plt
    from Modules.chart import add_labels
    
    print(data)

    Ingredient = data['Ingredient']
    Price = data.iloc[:,1]

    plt.bar(Ingredient,Price)
    
    add_labels(Ingredient, Price)
    
    plt.title("Price")
    
    plt.xlabel("Ingredients")
    plt.ylabel("Priser")
    plt.xticks(rotation='vertical')
    
    plt.show()
    
def calculate_price_of_top_three(csv_file1, csv_file2, csv_file3):
    """
    This function calculates the sum of price in the three recipes given as an argument.
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from Modules.chart import make_autopct
    
    price_1 = merge_price(csv_file1)     
    price_2 = merge_price(csv_file2)
    price_3 = merge_price(csv_file3)  

    price_sum1 = price_1["Price"].sum()
    price_sum2 = price_2["Price"].sum()
    price_sum3 =price_3["Price"].sum()
    
    #values =sorted(np.array([price_sum1, price_sum2,price_sum3]))
    values =np.array([price_sum1, price_sum2,price_sum3])
    labels = ["recipe1", "recipe2","recipe3"]
    colors = ["lightskyblue", "dodgerblue","royalblue"]

    plt.pie(values, labels = labels, colors = colors, autopct=make_autopct(values), shadow=True)
    plt.title("Price")
    #plt.legend()
    plt.show() 