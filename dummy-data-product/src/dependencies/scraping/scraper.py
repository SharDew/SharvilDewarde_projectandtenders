import pandas as pd
from bs4 import BeautifulSoup
import requests


class WebScraper:
    def __init__(self):
        self.p_title = []
        self.result = []
        self.open_bid = []
        self.description = []
        self.url = "https://www.chinabidding.com/en/info/search.htm"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        }

    def scrape(self):
        page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")
        title_tag = soup.find_all("a", class_="item-title-text bold fs18")
        title = [t.text for t in title_tag]
        links_url = []
        for links in title_tag:
            links_url.append(links["href"])

        for l in links_url:
            new_url = l
            link_r = requests.get(new_url, headers=self.headers)
            link_soup = BeautifulSoup(link_r.content, "html.parser")
            project_name_tag = link_soup.find(
                "p", class_="text-center detail-title"
            ).text
            project_name = project_name_tag if project_name_tag else "Null"

            self.p_title.append(project_name)
            project = link_soup.find("div", class_="main-info")
            lines = project.get_text(separator="\n").split("\n")
            for line in lines:
                try:
                    if "Bidding Content:" in line:
                        self.description.append(line.strip("Bidding Content:"))
                    if "Open-Time of Bids:" in line:
                        self.open_bid.append(line.strip("Open-Time of Bids:"))
                    if "Ending Date of Evaluation Result:" in line:
                        self.result.append(
                            line.strip("Ending Date of Evaluation Result:")
                        )
                except AttributeError as e:
                    if "Bidding Content:" in line:
                        self.description.append(e)
                    if "Open-Time of Bids:" in line:
                        self.open_bid.append(e)
                    if "Ending Date of Evaluation Result:" in line:
                        self.result.append(e)

        print(
            len(self.result),
            len(self.open_bid),
            len(self.description),
            len(self.p_title),
        )

        output = {
            "Project Title": self.p_title,
            "Project Description": self.description,
            "Bid Opening": self.open_bid,
            "Result Date": self.result,
        }

        max_len = max(
            len(l) for l in [self.p_title, self.description, self.open_bid, self.result]
        )
        if len(self.p_title) < max_len:
            self.p_title += [""] * (max_len - len(self.p_title))
        if len(self.description) < max_len:
            self.description += [""] * (max_len - len(self.description))
        if len(self.open_bid) < max_len:
            self.open_bid += [""] * (max_len - len(self.open_bid))
        if len(self.result) < max_len:
            self.result += [""] * (max_len - len(self.result))

        output = {
            "Project Title": self.p_title,
            "Project Description": self.description,
            "Bid Opening": self.open_bid,
            "Result Date": self.result,
        }

        df = pd.DataFrame(output)
        new_df = df.fillna(
            {
                "Project Description": "Not mentioned",
                "Bid Opening": "Null",
                "Result Date": "NaN",
            }
        )
        new_df.to_csv("Out.csv")


if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape()
