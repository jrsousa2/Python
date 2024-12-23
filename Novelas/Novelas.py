import requests
from bs4 import BeautifulSoup

# URL of the page
url_example = "https://pt.wikipedia.org/wiki/O_%C3%89brio"

def Read_URL(url):
    # Fetch the page content
    response = requests.get(url)

    if response.status_code == 200:  # Success
        # Process the content
        page_text = response.text

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table or section containing the names and characters
        table = soup.find('table', {'class': 'wikitable sortable'})

        # Extracting rows of the table
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 2:  # Assuming two columns (Ator, Personagem)
                actor = columns[0].get_text(strip=True)
                character = columns[1].get_text(strip=True)
                print(f'{actor}: {character}')
        print()        
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

