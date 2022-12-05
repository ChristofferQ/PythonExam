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
    
    return df  
            
def search_for_recipes_by_ingredient():
    """
    This function is used to input the name of an ingredient and show the names
    of recepies containing that ingredient
    """
    import bs4
    import requests
    import pandas as pd
    from Modules.populate_data import populate_missing_ingredients
    
    r = requests.get('https://www.webopskrifter.dk/503/')
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    listItems = soup.find('section', {'class':'deepnav'})

    #Skaber to tomme lister til at indeholde vores værdier.
    Values = [] #Url på ingredienser
    Keys = [] #Navn på ingredienser

    #Tiføjer url til values
    for link in listItems.find_all('a'):
        Values.append(link.get('href'))

    #Tilføjer ingrediens navne til keys
    for sp in soup.find_all('span', itemprop="name"):
        Keys.append(sp.text)

    ingredientsDict = {} #Dictionary til ingredienser

    #Tilføjer vores values og keys til dictionary
    for i in range(len(Keys)):
        ingredientsDict[Keys[i]] = Values[i]
        
    #Bruger input til at angive hvilken key vi søger efter, så vi kan sætte dens value som variablen searchIngredient, der bruges efterfølgende til at finde opskrift siden
    searchIngredient = ingredientsDict[input("Your ingredient: ")]
    
    #This is horrible, don't keep it 
    print('')

    r2 = requests.get('https://www.webopskrifter.dk/' + searchIngredient)
    r2.raise_for_status()
    soup = bs4.BeautifulSoup(r2.content, 'html.parser')
    
    i = 1
    
    Values2 = [] #Url på opskrifter
    Keys2 = [] #Navn på opskrifter

    #Tilføjer opskrifternes navne til Keys og printer navnene på opskrifterne med et tilføjet tal foran
    for sp in soup.find_all('span', class_="h3-size"):
        print(i, '\t', (sp.text))
        Keys2.append(i)
        i+=1
        
    #Finder url på opskrifterne    
    for sp in soup.find_all('div', class_="col_3-5"):
        Values2.append(sp.find('a').get('href'))
        
    recipesDict = {} #Dictionary til opskrifter
        
    #Lav en ny dictionary med key = i og value = url til de enkelte opskrifter
    for i in range(len(Keys2)):
        recipesDict[Keys2[i]] = Values2[i]
     
    #Gemmer top tre recipes i adskilte filer
    df1 = save_recipe(1, recipesDict)
    df1.to_csv('./Data/recipe1.csv', index=False)
    
    df2 = save_recipe(2, recipesDict)
    df2.to_csv('./Data/recipe2.csv', index=False)
    
    df3 = save_recipe(3, recipesDict)
    df3.to_csv('./Data/recipe3.csv', index=False)
    
    #This is horrible, don't keep it 
    print('')
    
    #Her vælger vi en bestemt opskrift givet dens key som blot er et tal (i som vi tilføjede)
    input_ = input("Your recipe:")
    searchRecipe = recipesDict[int(input_)]
    
    #Gemmer den valgte opskrift i recipe_ingredients.csv via save_recipe() metoden
    df = save_recipe(int(input_), recipesDict)
    df.to_csv('./Data/recipe_ingredients.csv', index=False)

    #Printer opskriftens ingredienser
    print(df)
    
    #Printer opskriftens instruktioner
    for sp in soup.find_all('div', class_="instructions-text"):
            print(sp.text)
    
    populate_missing_ingredients()
    
