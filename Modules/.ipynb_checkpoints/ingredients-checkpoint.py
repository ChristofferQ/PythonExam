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

    #Tilføjer vores values og keys til dictionary
    for i in range(len(Keys)):
        ingredientsDict[Keys[i]] = Values[i]
    
    #Bruger input til at angive hvilken key vi søger efter, så vi kan sætte dens value som variablen insert_ der bruges efterfølgende til at finde opskrift siden
    searchIngredient = ingredientsDict[input("Your ingredient: ")]

    insert = searchIngredient

    r2 = requests.get('https://www.webopskrifter.dk/' + insert)
    r2.raise_for_status()
    soup = bs4.BeautifulSoup(r2.content, 'html.parser')
    
    i = 1

    #Printer navnene på opskrifterne med et tilføjet tal foran
    for sp in soup.find_all('span', class_="h3-size"):
        print(i, '\t', (sp.text))
        i+=1
        
        
def get_content_of_recipe():
    """
    
    """
    