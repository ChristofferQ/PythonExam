def get_all_ingredients():
    import bs4
    import requests

    r = requests.get('https://www.webopskrifter.dk/503/')
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    for sp in soup.find_all('span',itemprop="name"):
            print(sp.text)
