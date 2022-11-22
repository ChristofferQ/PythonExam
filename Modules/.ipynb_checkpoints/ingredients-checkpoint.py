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

    Dict = {}

    #Tilføjer vores values og keys til dictionary
    for i in range(len(Keys)):
        Dict[Keys[i]] = Values[i]
    
    searchIngredient = Dict[input("Input your ingredient")]

    insert_ = searchIngredient

    r2 = requests.get('https://www.webopskrifter.dk/' + insert_)
    r2.raise_for_status()
    soup = bs4.BeautifulSoup(r2.content, 'html.parser')

    for sp in soup.find_all('span', class_="h3-size"):
        print(sp.text)