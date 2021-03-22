import bs4
import requests
import time


from dotenv import load_dotenv

from db import DB

URL = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"

def get_anecdotes():
    content = requests.get(URL)
    anecdotes = []
    if content.status_code == 200:
        page = bs4.BeautifulSoup(content.text, 'html.parser')
        pg = page.find('div', class_='portail-gauche')
        misc = pg.find_all('div', class_='accueil_2017_cadre')
        ul = misc[2].find('ul')
        lis = ul.find_all('li')
        for li in lis:
            s = ''
            for elem in li:
                try:
                    s += elem.text
                except AttributeError:
                    s += elem
            anecdotes.append(s)
    return anecdotes

        
def main():
    load_dotenv()
    anecdotes = get_anecdotes()
    with DB() as db:
        db.create_table()
        timing = round(time.time())
        for anecdote in anecdotes:
            db.add_entry_to_trivia(anecdote, timing)

if __name__ == '__main__':
    main()