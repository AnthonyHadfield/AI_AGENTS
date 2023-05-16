import requests
from bs4 import BeautifulSoup
from tkinter import *


class SearchScraper:
    def __init__(self, search_term):
        self.search_term = search_term
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }

    def scrape(self):
        response = requests.get(f"https://www.bing.com/search?q={self.search_term}", headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("li", class_="b_algo")
        return results

    def remove_duplicates(self, links):
        unique_links = []
        for link in links:
            if link not in unique_links:
                unique_links.append(link)
        return unique_links

    def display_results(self):
        root = Tk()
        root.title("Search Results")
        root.geometry("800x600")

        text_widget = Text(root)
        text_widget.pack(fill=BOTH, expand=True)

        link_list = []  # To store the links for the numbered list

        for i, result in enumerate(self.scrape(), 1):
            title = result.find("h2").text
            link = result.find("a")["href"]
            snippet = result.find("p").text

            text_widget.insert(END, f"Title: {title}\nLink: {link}\nDescription: {snippet}\n\n")
            link_list.append(link)

        # Remove duplicate links
        unique_links = self.remove_duplicates(link_list)

        # Add links at the bottom with numbering
        text_widget.insert(END, "\n\nWeb Links:\n")
        for i, link in enumerate(unique_links, 1):
            text_widget.insert(END, f"{i}. {link}\n")

        root.mainloop()


if __name__ == "__main__":
    search_term = input("Enter a search term: ")
    scraper = SearchScraper(search_term)
    scraper.display_results()