import os
import json
import csv
import openai
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INPUT_FILE = "fetched_bills_full.json"
OUTPUT_FILE = "processed_bills.csv"

openai.api_key = OPENAI_API_KEY

def simplify_text(text):
    """
    Simplify the legal text using OpenAI GPT-4.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Simplify this legal text into plain language."},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error simplifying text: {e}")
        return "Error simplifying text."

def extract_expenditures(text):
    """
    Extract expenditures and their purposes from the text.
    """
    expenditure_pattern = r"(\$\d+(?:,\d{3})*(?:\.\d+)?(?:\s(?:million|billion|trillion))?)"
    matches = re.findall(expenditure_pattern, text)
    return matches

def process_bills():
    """
    Process fetched bills to create simplified summaries and extract expenditures, and save as a CSV.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r") as infile:
        bills = json.load(infile)

    # Prepare data for CSV
    processed_bills = []
    for bill in bills:
        try:
            full_text = bill.get("fullText", "No full text available")
            simplified_summary = simplify_text(full_text)
            expenditures = extract_expenditures(full_text)
            processed_bills.append({
                "Bill ID": bill.get("billId", "Unknown ID"),
                "Title": bill.get("title", "No Title"),
                "Simplified Summary": simplified_summary,
                "Expenditures": "; ".join(expenditures)
            })
        except Exception as e:
            print(f"Error processing bill: {e}")

    # Write to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Bill ID", "Title", "Simplified Summary", "Expenditures"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(processed_bills)

    print(f"Processed {len(processed_bills)} bills and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_bills()
