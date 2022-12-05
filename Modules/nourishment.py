def merge_nourishment(csv_file):
    """
    This function merges the given file with ingredients_nourishment.csv and returns the result.
    """
    import pandas as pd

    df1 = pd.read_csv('./Data/ingredients_nourishment.csv')
    df2 = pd.read_csv('./Data/' + csv_file + '.csv')

    result = pd.merge(df1,df2) 
    
    return result

def get_nourishment_of_ingredients(csv_file):
    """
    This function uses merge_nourishment() to get ingredients individual nourishment and show_nourishment_of_ingredients() to display the result.
    """
    import pandas as pd

    result = merge_nourishment(csv_file)
    show_nourishment_of_ingredients(result)
    
def show_nourishment_of_ingredients(data):
    """
    This function displays the data from the given dataset by printing it and displaying it in a bar chart.
    """
    import pandas as pd 
    import matplotlib.pyplot as plt
    from Modules.chart import add_labels
    
    print(data)

    Ingredient = data['Ingredient']
    Kcal = data.iloc[:,1]

    plt.bar(Ingredient,Kcal, color = "sandybrown")
    
    add_labels(Ingredient,Kcal)
    
    plt.title("Nourishment")
    plt.xlabel("Ingredients")
    plt.ylabel("Kcal")
    plt.xticks(rotation='vertical')

    
    plt.show()
    
def calculate_nourishment_of_top_three(csv_file1, csv_file2, csv_file3):
    """
    This function calculates the sum of nourishment in the three recipes given as an argument.
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from Modules.chart import make_autopct
    
    
    nourish_1 = merge_nourishment(csv_file1)
    nourish_2 = merge_nourishment(csv_file2)
    nourish_3 = merge_nourishment(csv_file3)
    
    nourish_sum1 = nourish_1["Kcal"].sum()
    nourish_sum2 = nourish_2["Kcal"].sum()
    nourish_sum3 = nourish_3["Kcal"].sum()
    
    values = np.array([nourish_sum1, nourish_sum2, nourish_sum3])
    labels = ["recipe1", "recipe2","recipe3"]
    colors = ["sandybrown", "darksalmon","peru"]
    
    plt.pie(values, labels = labels, colors = colors, autopct=make_autopct(values), shadow=True)
    plt.title("Nourishment")
    #plt.legend()
    plt.show() 