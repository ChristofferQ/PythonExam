def get_all_ingredients():
    """
    This function is used to print all ingredient names from webopskrifter.dk
    """
    import bs4
    import requests

    r = requests.get('https://www.webopskrifter.dk/503/')
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    for sp in soup.find_all('span',itemprop="name"):
            print(sp.text)
            
#__________________________________________________________________________________________________________________________________________
            
def save_recipe(key, Dict):
    """
    This function is used to save the given recipe by key as csv file. 
    """
    import bs4
    import requests
    import pandas as pd
    
    searchRecipe = Dict[key]
    
    r = requests.get('https://www.webopskrifter.dk/' + searchRecipe)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
        
    Ingredient = []
    Unit = []
    Meassurement = []
    
    soup1 = soup.find_all('li',{'class':'ingredient'})

    for item in soup1:

        try:
            Meassurement.append(item.find('span', class_="num").text)
        except:
            Meassurement.append(None)

        try:
            Unit.append(item.find('span',class_='unit').text)
        except:
            Unit.append(None)

        try:
            Ingredient.append(item.find('span',class_='ingredientName').text.capitalize())
        except:
            Ingredient.append(None)

    df = pd.DataFrame(list(zip(*[Meassurement, Unit, Ingredient])), columns = ['Meassurement', 'Unit', 'Ingredient'])

    df.to_csv('./Data/Recipe' +str(key)+ '.csv', index=False)
    
#__________________________________________________________________________________________________________________________________________
            
def search_for_recipes_by_ingredient():
    """
    This function is used to input the name of an ingredient and show the names
    of recepies containing that ingredient
    """
    import bs4
    import requests
    import pandas as pd
    
    r = requests.get('https://www.webopskrifter.dk/503/')
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    listItems = soup.find('section', {'class':'deepnav'})

    #Skaber to tomme lister til at indeholde vores værdier.
    Values = [] #Url på ingrediens
    Keys = [] #Navn til ingrediens 

    #Tiføjer url til values
    for link in listItems.find_all('a'):
        Values.append(link.get('href'))

    #Tilføjer ingrediens navne til keys
    for sp in soup.find_all('span', itemprop="name"):
        Keys.append(sp.text)

    ingredientsDict = {}
    recipesDict = {}

    #Tilføjer vores values og keys til dictionary
    for i in range(len(Keys)):
        ingredientsDict[Keys[i]] = Values[i]
        
    #Bruger input til at angive hvilken key vi søger efter, så vi kan sætte dens value som variablen insert_ der bruges efterfølgende til at finde opskrift siden
    searchIngredient = ingredientsDict[input("Your ingredient: ")]
    
    #This is horrible, don't keep it 
    print('')

    r2 = requests.get('https://www.webopskrifter.dk/' + searchIngredient)
    r2.raise_for_status()
    soup = bs4.BeautifulSoup(r2.content, 'html.parser')
    
    i = 1
    
    Values2 = []
    Keys2 = []

    #Printer navnene på opskrifterne med et tilføjet tal foran
    for sp in soup.find_all('span', class_="h3-size"):
        print(i, '\t', (sp.text))
        Keys2.append(i)
        i+=1
        
        
    for sp in soup.find_all('div', class_="col_3-5"):
        Values2.append(sp.find('a').get('href'))
        
    #Lav en ny dictionary med key = i og value = url til de enkelte opskrifter
    for i in range(len(Keys2)):
        recipesDict[Keys2[i]] = Values2[i]
     
    #Gemmer top tre recipes i adskilte filer
    save_recipe(1, recipesDict)
    save_recipe(2, recipesDict)
    save_recipe(3, recipesDict)
    
    
    #This is horrible, don't keep it 
    print('')
        
    
    
    #Så vi kan lave en ny input, der bliver til et nyt kald i hjemmeside med url for den valgte opksrift
    #searchRecipe = recipesDict[input("Her:")]
    searchRecipe = recipesDict[int(input("Your recipe:"))]
    
    
    r3 = requests.get('https://www.webopskrifter.dk/' + searchRecipe)
    r3.raise_for_status()
    soup = bs4.BeautifulSoup(r3.content, 'html.parser')
    
        #Outcommenting this for now, to use lists instead, so we can save itto a csv file
        #for sp in soup.find_all('li',itemprop="recipeIngredient"):
        #    print(sp.text)

        #for sp in soup.find_all('div', class_="instructions-text"):
        #    print(sp.text)
        
    Ingredient = []
    Unit = []
    Meassurement = []
    
    soup1 = soup.find_all('li',{'class':'ingredient'})

    for item in soup1:

        try:
            Meassurement.append(item.find('span', class_="num").text)
        except:
            Meassurement.append(None)

        try:
            Unit.append(item.find('span',class_='unit').text)
        except:
            Unit.append(None)

        try:
            Ingredient.append(item.find('span',class_='ingredientName').text.capitalize())
        except:
            Ingredient.append(None)
        
    #Vi skal gemme ingredienserne i en Dictionary, så vi kan bruge dem til at søge på f.eks. nemlig.com og hente priser 
    #for de individuelle ingredienser, på den måde kan vi både vise prisen for hver enkelt ingrediens og vise summen af 
    #hele indkøbet 
    
    #This is horrible, don't keep it 
    print('')
    


    #Lists from earlier, Meassurement, Unit, Ingredient

    df = pd.DataFrame(list(zip(*[Meassurement, Unit, Ingredient])), columns = ['Meassurement', 'Unit', 'Ingredient'])

    df.to_csv('./Data/recipe_ingredients.csv', index=False)

    print(df)
    
    for sp in soup.find_all('div', class_="instructions-text"):
            print(sp.text)
            
#__________________________________________________________________________________________________________________________________________

def merge_price(csv_file):
    """
    This function merges the given file with ingredients_prices.csv and returns the result.
    """
    import pandas as pd
    
    df1 = pd.read_csv('./Data/ingredients_prices.csv')
    df2 = pd.read_csv('./Data/' + csv_file + '.csv')
    
    result = pd.merge(df1,df2)
    
    return result

#__________________________________________________________________________________________________________________________________________

def get_price_of_ingredients(csv_file):
    """
    This function uses merge_price() to get ingredients individual price and show_price_of_ingredients() to display the result.
    """
    import pandas as pd

    result = merge_price(csv_file)
    show_price_of_ingredients(result)
    
#__________________________________________________________________________________________________________________________________________

def show_price_of_ingredients(data):
    """
    This function displays the data from the given dataset by printing it and displaying it in a bar chart.
    """
    import pandas as pd 
    import matplotlib.pyplot as plt
    
    print(data)

    Ingredient = data['Ingredient']
    Price = data.iloc[:,1]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(Ingredient,Price)
    
    add_labels(Ingredient, Price)
    
    plt.title("Show me the money!")
    plt.xlabel("Ingredients")
    plt.ylabel("Priser")

    
    plt.show()
    
#__________________________________________________________________________________________________________________________________________
    
def add_labels(x,y):
    """
    Add labels to barplot.
    """
    import matplotlib.pyplot as plt
    
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')
        
#__________________________________________________________________________________________________________________________________________

def merge_nourishment(csv_file):
    """
    This function merges the given file with ingredients_nourishment.csv and returns the result.
    """
    import pandas as pd

    df1 = pd.read_csv('./Data/ingredients_nourishment.csv')
    df2 = pd.read_csv('./Data/' + csv_file + '.csv')

    result = pd.merge(df1,df2) 
    
    return result
    
#__________________________________________________________________________________________________________________________________________

def get_nourishment_of_ingredients(csv_file):
    """
    This function uses merge_nourishment() to get ingredients individual nourishment and show_nourishment_of_ingredients() to display the result.
    """
    import pandas as pd

    result = merge_nourishment(csv_file)
    show_nourishment_of_ingredients(result)
    
#__________________________________________________________________________________________________________________________________________
    
def show_nourishment_of_ingredients(data):
    """
    This function displays the data from the given dataset by printing it and displaying it in a bar chart.
    """
    import pandas as pd 
    import matplotlib.pyplot as plt
    
    print(data)

    Ingredient = data['Ingredient']
    Kcal = data.iloc[:,1]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(Ingredient,Kcal)
    
    add_labels(Ingredient,Kcal)
    
    plt.title("Show me the Ermin!")
    plt.xlabel("Ingredients")
    plt.ylabel("Kcal")

    
    plt.show()
    
#__________________________________________________________________________________________________________________________________________
    
    
def get_price_and_nourishment_for_ingredients():
    """
    Does it all baby
    """
    import pandas as pd

    df1 = pd.read_csv('./Data/recipe_ingredients.csv')
    df2 = pd.read_csv('./Data/ingredients_prices.csv')
    df3 = pd.read_csv('./Data/ingredients_nourishment.csv')

    result = df1.merge(df2).merge(df3)

    print(result)
    
    #show_nourishment_and_price_of_ingredient(result)
    
#__________________________________________________________________________________________________________________________________________
    
def show_nourishment_and_price_of_ingredient(data):
    """
    Vær's'god Ermin
    """
    
#__________________________________________________________________________________________________________________________________________

def calculate_price_of_top_three(csv_file1, csv_file2, csv_file3):
    """
    This function calculates the sum of price and the sum of Kcal in the three recipes given as an argument.
    """
    import pandas as pd
    
    price_1 = merge_price(csv_file1)     
    price_2 = merge_price(csv_file2)
    price_3 = merge_price(csv_file3)  

    print(price_1["Price"].sum())
    print(price_2["Price"].sum())
    print(price_3["Price"].sum())
    
    nourish_1 = merge_nourishment(csv_file1)
    nourish_2 = merge_nourishment(csv_file2)
    nourish_3 = merge_nourishment(csv_file3)
    
    print(nourish_1["Kcal"].sum())
    print(nourish_2["Kcal"].sum())
    print(nourish_3["Kcal"].sum())
    