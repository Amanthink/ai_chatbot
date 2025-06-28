import requests
from bs4 import BeautifulSoup

def scrape_static(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [p.get_text(strip=True) for p in soup.find_all('p')]

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    data = scrape_static(url)
    with open("../data/raw_text.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(data))
