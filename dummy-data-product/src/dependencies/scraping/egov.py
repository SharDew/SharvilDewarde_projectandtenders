import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website from which data is to be scraped
class Scraper:
    def __init__(self):
        self.url = "https://etenders.gov.in/eprocure/app"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        }

    def get_data(self):
        r = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", class_="list_table")
        table_info = soup.find("table", id="activeTenders")
        table_titles = table.find("tr", class_="list_header")
        titles = table_titles.find_all("td")
        t_cols = [t.text for t in titles]
        t_titles = table_info.find_all("a", class_="link2")
        tender_titles = [tender.text for tender in t_titles]
        num = table_info.find_all("td", attrs={"width": "20%"})
        reference_number = [ref.text for ref in num]
        closing_date = [
            tr.find_all("td")[2].text.strip()
            for tr in soup.find_all("tr", {"class": "even"})
        ]
        opening_bid = [
            tr.find_all("td")[3].text.strip()
            for tr in soup.find_all("tr", {"class": "even"})
        ]
        table_data = [tender_titles, reference_number, closing_date, opening_bid]
        table = {k: v for k, v in zip(t_cols, table_data)}
        df = pd.DataFrame.from_dict(table)
        df.to_csv("Output_Bharat.csv")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.get_data()
