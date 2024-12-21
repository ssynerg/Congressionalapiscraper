# fetch_bills.py
import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()
congress_api_key = os.getenv('CONGRESS_API_KEY')

def fetch_bills(congress, bill_type, limit=50):
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}?limit={limit}&format=json&api_key={congress_api_key}'
    print(f"Using API Key: {congress_api_key}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('bills', [])
    else:
        print(f'Error fetching bills: {response.status_code} - {response.text}')
        return []

def save_bills_to_csv(bills, filename='bills.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Bill Number', 'Title', 'API URL', 'Congress.gov URL'])
        for bill in bills:
            bill_number = bill.get('number')
            title = bill.get('title', 'No Title Provided')
            api_url = bill.get('url')
            congress = bill.get('congress')
            congress_url = f"https://www.congress.gov/bill/{congress}th-congress/house-bill/{bill_number}/text"
            writer.writerow([bill_number, title, api_url, congress_url])

if __name__ == "__main__":
    bills = fetch_bills(congress=118, bill_type='hr', limit=50)
    if bills:
        save_bills_to_csv(bills)
    else:
        print("No bills were fetched.")
