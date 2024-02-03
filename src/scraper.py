import requests
from bs4 import BeautifulSoup as bs
import re
import json 

class WikipediaScraper:
    def __init__(self, base_url:str, country_endpoint:str, leaders_endpoint:str,
                cookies_endpoint:str, leaders_data:dict=None, cookie=None):
        
        self.cookie = None
        self.base_url = base_url
        self.country_endpoint = country_endpoint
        self.leaders_endpoint = leaders_endpoint
        self.cookies_endpoint = cookies_endpoint
        self.leaders_data = {}
        self.paragraph_counter = 0
        self.countries = {}
        self.all_data = {}

    def refresh_cookie(self):
        """
        Refreshes the cookie (which is used for authentication during API requests.)
        when the cookie has expired. 
        """

        cookie_url = self.base_url + self.cookies_endpoint
        cookie_req = requests.get(cookie_url)
        if cookie_req.status_code == 200:
            self.cookie = cookie_req.cookies
            print("Connection to the server was successful.")            
        else:
            print(f"Connection failed with error code: {cookie_req.status_code}."
                   "For further explanation, please visit:"
                   "https://en.wikipedia.org/wiki/List_of_HTTP_status_codes")
        
    def get_countries(self) -> dict:
        """
        Retrieves a list of all the countries from the API
        and assigns them to the attribute 'self.countries'.
        """

        COUNTRY_NAMES = {
        'us': 'United States',
        'be': 'Belgium', 
        'fr': 'France', 
        'ma': 'Morocco', 
        'ru': 'Russia'
    }
        country_url = self.base_url + self.country_endpoint
        country_req = requests.get(country_url, cookies=self.cookie)

        if country_req.status_code == 200:
            country_codes = country_req.json()  
            self.countries = {code: COUNTRY_NAMES.get(code, code) for code 
                              in country_codes}
            return self.countries
        else:
            self.refresh_cookie()
            country_req = requests.get(country_url)
            if country_req.status_code == 200:
                country_codes = country_req.json
                self.countries = {code: COUNTRY_NAMES.get(code, code) for code
                                   in country_codes}
                return self.countries
            else:  
                raise Exception("Failed to get countries from API. ")

    def get_leaders(self, country:str) -> dict:
        """
        Retrieves the first and last names of each leader, along with their Wikipedia URLs, 
        for a specific country from the API. If there are leaders with the same first and last name,
        a suffix is added to distinguish them (e.g., 'FirstName lastName_1', 'FirstName LastName_2', etc.).
        This is done because a dictionary key is unique and can't occur twice in the same dict.
        """

        leaders_url = self.base_url + self.leaders_endpoint
        leader_req = requests.get(leaders_url, cookies=self.cookie, params={"country":country})

        if leader_req.status_code == 200:
            leaders_data = leader_req.json()
            self.leaders_data = {}
            for leader in leaders_data:
                key = f"{leader['first_name']} {leader['last_name']}"
                if key in self.leaders_data:
                    i = 1
                    while f"{key}_{i}" in self.leaders_data:
                        i += 1
                    key = f"{key}_{i}"
                self.leaders_data[key] = leader['wikipedia_url']
            return self.leaders_data
        else:
            self.refresh_cookie()
            leader_req = requests.get(leaders_url, cookies=self.cookie, params={"country":country})
            if leader_req.status_code == 200:
                leaders_data = leader_req.json()
                self.leaders_data = {}
                for leader in leaders_data:
                    key = f"{leader['first_name']} {leader['last_name']}"
                    if key in self.leaders_data:
                        i = 1
                        while f"{key}_{i}" in self.leaders_data:
                            i += 1
                        key = f"{key}_{i}"
                    self.leaders_data[key] = leader['wikipedia_url']
                return self.leaders_data
            else:
                raise Exception("Failed to retrieve leaders data.")

            
    def test_urls(self):
        """
        Tests each leaders URL by sending a request and checking the response.
        Prints a message indicating whether each URL is responding correctly.
        """

        countries = self.get_countries()
        counter_positive = 0
        counter_negative = 0
        for country in countries:
            urls = self.get_leaders(country) 
            for url in urls.values():
                response = requests.get(url).status_code
                if response == 200:
                    counter_positive += 1
                    print(f"URL {url} is working correctly.")
                else:
                    counter_negative += 1
                    print(f"URL {url} returned an error with status code"
                           "{response}.")
        print(f"{counter_positive} URLs returned status code 200 (OK).")
        print(f"{counter_negative} URLs returned an error.")

    @staticmethod
    def get_key_from_value(dictionary, value):
        """
        Returns the key corresponding to a given value in a specific dictionary.
        """
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    def get_first_paragraph(self, url: str) -> str:
        """
        Extracts the first paragraph from the leaders WikiPedia page,
        which contains a short description of the leader leader.
        """
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        
        paragraphs = soup.find_all('p')
        first_paragraph_text = None

        for paragraph in paragraphs:
            if paragraph.find('b'):
                first_paragraph_text = paragraph.get_text().strip()
                break

        if first_paragraph_text:
            cleaned_paragraph = self.clean_paragraph(first_paragraph_text)
            print(f"First paragraph from WikiPedia page:\n\n{cleaned_paragraph}")
            return cleaned_paragraph
        else:
            print("No meaningful content found in the first paragraph.")
            return "No meaningful content found"


    def clean_paragraph(self, paragraph: str) -> str:
        """ 
        This method cleans the data scraped from wikipedia
        by removing extra spaces and pronunciation guides from the paragraph. 
        """
        cleaned_paragraph = re.sub(r'\(.*?\)', '', paragraph)
        # Remove multiple spaces
        cleaned_paragraph = re.sub(r'\s+', ' ', cleaned_paragraph)
        return cleaned_paragraph.strip()


    def to_json_file(self, filepath: str) -> None:
        """
        Stores all scraped data into a JSON file at the specified filepath.
        The data is formatted with an indent of 2 spaces for readability, 
        and non-ASCII characters are preserved.
        """
        with open(filepath, 'w') as f:
            json.dump(self.all_data, f, indent=2, ensure_ascii=False)

        