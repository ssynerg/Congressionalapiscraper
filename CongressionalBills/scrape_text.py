import os
import json
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "fetched_bills_full.json"
OUTPUT_FILE = "fetched_bills_with_text.json"

def convert_to_congress_url(api_url):
    """
    Convert an API URL into a Congress.gov bill text URL.
    """
    parts = api_url.split('/')
    congress_number = parts[-3]
    bill_type = parts[-2]
    bill_number = parts[-1].split('?')[0]
    return f"https://www.congress.gov/bill/{congress_number}th-congress/{bill_type}/{bill_number}/text"

def scrape_congress_text(congress_url):
    """
    Scrape the bill text from the Congress.gov URL.
    """
    try:
        response = requests.get(congress_url)
        if response.status_code != 200:
            print(f"Error fetching text from {congress_url}: {response.status_code}")
            return "Full text not available"
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Locate the bill text section (adjust based on actual Congress.gov structure)
        text_section = soup.find('div', class_='generated-html-container')
        if text_section:
            return text_section.get_text(strip=True)

        # If specific formats are available (XML, TXT, PDF), download and process them
        formats = soup.find_all('a', string=["XML", "TXT", "PDF"])
        for fmt in formats:
            format_url = fmt['href']
            if 'txt' in format_url.lower():
                return requests.get(format_url).text  # For plain text
            elif 'pdf' in format_url.lower():
                # Download PDF and convert (placeholder for PDF handling logic)
                return "PDF format detected but not processed"
            elif 'xml' in format_url.lower():
                # Process XML (placeholder for XML handling logic)
                return "XML format detected but not processed"

        return "Full text not available"
    except Exception as e:
        print(f"Error scraping Congress text: {e}")
        return "Full text not available"

def scrape_full_text():
    """
    Read fetched bills, scrape their full text, and save updated data.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r") as infile:
        bills = json.load(infile)

    for bill in bills:
        api_url = bill.get("url")
        if api_url:
            congress_url = convert_to_congress_url(api_url)
            print(f"Scraping text for bill: {bill.get('number')} ({bill.get('title')}) from {congress_url}")
            bill["fullText"] = scrape_congress_text(congress_url)
        else:
            bill["fullText"] = "Full text URL not available"

    # Save updated bills with full text to a new JSON file
    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(bills, outfile, indent=4)
    print(f"Scraped full text for {len(bills)} bills and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_full_text()
