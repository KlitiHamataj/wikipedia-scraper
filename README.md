# Wikipedia Scraper 🌍

A Python scraper that retrieves political leaders for each country from an API, then scrapes their first Wikipedia paragraph and saves everything to a JSON file.

---------

## What does it do

1. Calls the (https://country-leaders.onrender.com) API to get a list of countries and their leaders
2. For every leader it scrapes thei Wikipedia page and extract the first paragraph form their bio
3. Cleans the text (removes citations like `[1]`, extra whitespace, etc.)
4. Saves all the updated data into a JSON file

----------

## Project Structure

```
wikipedia-scraper/
├── venv/                   
├── wikipedia_scraper.py     
├── main.py                  
├── leaders.json             
├── requirements.txt         
└── README.md
```

---------

## How to install it

### 1. Clone the repo

```bash
git clone https://github.com/KlitiHamataj/wikipedia-scraper.git
cd wikipedia-scraper
```

### 2. create and activate the virtual environment

```bash
python -m venv venv
source venv/bin/activate            # on windows venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---------

## Usage

```bash
python main.py
```

In the root of the project a `leaders.json` file will be generated

---------

## Output

```json
{
    "be": [
        {
            "id": "Q12978",
            "first_name": "Guy",
            "last_name": "Verhofstadt",
            "birth_date": "1953-04-11",
            "death_date": null,
            "place_of_birth": "Dendermonde",
            "wikipedia_url": "https://nl.wikipedia.org/wiki/Guy_Verhofstadt",
            "start_mandate": "1999-07-12",
            "end_mandate": "2008-03-20",
            "first_paragraph": "Guy Maurice Marie Louise Verhofstadt uitspraak Dendermonde 11 april 1953 is een Belgisch politicus voor de Open Vlaamse Liberalen en Democraten Open Vld Hij was premier van België van 12 juli 1999 tot 20 maart 2008 in drie regeringen Hij beëindigde zijn actieve politieke carrière in het Europees Parlement waar hij van 2009 tot 2019 fractieleider van de Alliantie van Liberalen en Democraten voor Europa ALDE was 6"
        },
}        
```

---------

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | Making HTTP calls to the API and Wikipedia |
| `beautifulsoup4` | Parsing Wikipedia HTML |

Everything else (`json`, `re`) is part of Python's standard library.

---------

## How it works

- Uses a `requests.Session()` to persist cookies automatically across requests
- Automatically refreshes the API cookie when it expires (403 response)
- Cleans the scraped text using `re.sub()` to remove citations and extra whitespace

---------

## Notes

- The API requires a valid cookie to access the `/leaders` endpoint — this is handled automatically
- `time.sleep(1)` is used between requests to avoid overwhelming the server
- `ensure_ascii=False` is used when saving JSON to correctly handle non-latin characters