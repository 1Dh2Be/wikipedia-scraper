# Wikipedia scraper 

## Program description

This program is designed to extract a short description of political leaders.
It communicates with a specific API to retrieve preparatory information, which is then used to scrape relevant data from political leaders Wikipedia page.
The data includes details about various countries and their leaders.

The program efficiently manages cookies for API authentication,
verifies the validity of URLs, and formats the scraped data for usability.
The final data is conveniently stored in a JSON file, ready for further analysis or research.

## Installations

This program presumes you already have python,
if not, visit the official website [here](https://www.python.org) to download python. 

#### 1. Clone the git repository on your local machine

```git clone git@github.com:1Dh2Be/wikipedia-scraper.git```

#### 2. Install Anaconda (if you already have Anaconda, skip to step 3)

To use the program, please set up the virtual environment.
The details of the virtual environment will be located in the '.gitignore' file or follow the steps underneath for guidance.

To proceed with the setup of the virtual environment, you'll need Anaconda.
If you've never heard of anaconda, visit [this](https://www.codeunderscored.com/beginners-guide-to-anaconda-python/) link for thorough explanation.

If you don't have Anaconda on your local machine, visit the official website [here](https://www.anaconda.com/download) to download it 

#### 3. Set up virtual environment

To install the virtual environment in order to use the program, follow the following command:

```conda env create -f wikienv.yml```

Lastly, you need to activate the environment, to do so, follow this commmand: 

```conda activate wikienv```

Congratulations! You're now all set up to use the program 🥳.

## Usage

- To run the program, simply type ```python main.py``` in terminal.
- A file will then be created with the first&last name, country and a small description of the leaders. 






