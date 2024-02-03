# Import the WikipediaScraper class from the scraper module
from src.scraper import WikipediaScraper

# This is the entry point of the script
if __name__ == "__main__":
    
    # Create an instance of the WikipediaScraper class
    # Initialize it with the base URL and endpoints for the API
    scraper = WikipediaScraper('https://country-leaders.onrender.com/',
                                'countries/', 'leaders/', 'cookie/')
    
    # Refresh the cookie to ensure we can connect to the API
    scraper.refresh_cookie()
    
    # Get a list of countries from the API
    countries = scraper.get_countries()

    # Create a new dictionary to hold all leaders' data
    scraper.all_data = {}

    # For each country...
    for country_code, country_name in countries.items():
        # Print a message to let the user know we're fetching the leaders for this country
        print(f"\nFetching leaders for {country_name}...")
        
        # Get the leaders for this country from the API
        leaders_data = scraper.get_leaders(country_code)
        
        # For each leader...
        for leader_name, url in leaders_data.items():
            # Print the leader's name and URL
            print(f"\nLeader: {leader_name}")
            print(f"URL: {url}")
            
            # Get the first paragraph from the leader's Wikipedia page
            first_paragraph = scraper.get_first_paragraph(url)

            # Update the leaders_data dictionary with the first paragraph
            scraper.all_data[leader_name] = first_paragraph
            

    # Save the leaders data to a JSON file
    scraper.to_json_file('test.json')
