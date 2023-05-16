import requests
from bs4 import BeautifulSoup
from tkinter import *


class SearchScraper:
    def __init__(self, search_term):
        self.search_term = search_term
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }

    def scrape(self):
        response = requests.get(f"https://www.google.com/search?q={self.search_term}", headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="g")

        unique_results = []
        unique_urls = set()

        for result in results:
            url = result.find("a")["href"]
            if url not in unique_urls:
                unique_results.append(result)
                unique_urls.add(url)

        return unique_results

    def display_results(self):
        root = Tk()
        root.title("Search Results")
        root.geometry("800x900")

        text_widget = Text(root)
        text_widget.pack(fill=BOTH, expand=True)

        link_list = []  # To store the links for the numbered list

        for i, result in enumerate(self.scrape(), 1):
            title = result.find("h3").text
            link = result.find("a")["href"]
            description_element = result.find("span", class_="aCOpRe")
            description = description_element.text if description_element else ""

            text_widget.insert(END, f"Title: {title}\nLink: {link}\nDescription: {description}\n\n")
            link_list.append(f"{i}. {link}")

        # Add links at the bottom with spacing
        link_text = "\n\n".join(link_list)
        text_widget.insert(END, "\n\nWeb Links:\n")
        text_widget.insert(END, link_text)

        root.mainloop()


if __name__ == "__main__":
    search_term = input("Enter a search term: ")
    scraper = SearchScraper(search_term)
    scraper.display_results()
