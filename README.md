# price-scraper-
Web scraper that extracts product data to CSV
# Price Scraper

A simple Python web scraper that extracts product data from [books.toscrape.com](https://books.toscrape.com/) and saves it to a CSV file.

## What it does

- Crawls multiple catalog pages
- Extracts title, price, and product link for each book
- Handles pagination and errors gracefully
- Saves results to `books.csv`

## Tech stack

- Python 3
- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing

## Setup

```bash
pip install requests beautifulsoup4