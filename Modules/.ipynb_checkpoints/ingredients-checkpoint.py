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
            
def get_price_of_ingredients():
    """
    This method is used to calculate the price of the ingredients from the recipe selected by the method search_for_recipes_by_ingredient()
    """
    #Vi skal lave en metode der tager ingredienserne fra recipe_ingredients.csv og matcher dem med ingredienser fra filen ingredients_prices.csv for at finde prisen og printer dem.
    import pandas as pd

    df1 = pd.read_csv('./Data/ingredients_prices.csv')
    df2 = pd.read_csv('./Data/recipe_ingredients.csv')

    result = pd.merge(df1,df2)

    print(result)
    
    show_price_of_ingredients(result)
                
    #Der tages ikke ikke højde for at nogle ingredienser kan mangle, der måtte den gerne vise navnet på manglende ingrediens, så vi kan få det tilføjet. 

def show_price_of_ingredients(data):
    """
    Given a dataframe, show bar plot
    """
    import pandas as pd 
    import matplotlib.pyplot as plt
    
    result = data

    Ingredient = result['Ingredient']
    Price = result.iloc[:,1]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(Ingredient,Price)
    
    add_labels(Ingredient, Price)
    
    plt.title("Show me the money!")
    plt.xlabel("Ingredients")
    plt.ylabel("Priser")

    
    plt.show()
    
def add_labels(x,y):
    """
    Add labels to barplot.
    """
    import matplotlib.pyplot as plt
    
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')
        
def get_nourishment_for_ingredients():
    """
    
    """
    import pandas as pd

    df1 = pd.read_csv('./Data/ingredients_nourishment.csv')
    df2 = pd.read_csv('./Data/recipe_ingredients.csv')

    result = pd.merge(df1,df2)

    print(result)
    
    show_nourishment_of_ingredients(result)
    
def show_nourishment_of_ingredients(data):
    """
    TBD
    """
    import pandas as pd 
    import matplotlib.pyplot as plt
    
    result = data

    Ingredient = result['Ingredient']
    Kcal = result.iloc[:,1]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(Ingredient,Kcal)
    
    add_labels(Ingredient,Kcal)
    
    plt.title("Show me the Ermin!")
    plt.xlabel("Ingredients")
    plt.ylabel("Kcal")

    
    plt.show()
    
    
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
    
def show_nourishment_and_price_of_ingredient(data):
    """
    Vær's'god Ermin
    """
    