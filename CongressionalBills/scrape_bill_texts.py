from playwright.sync_api import sync_playwright
import os
import time
import random
import csv

# Directory to store session data
SESSION_DIR = "./playwright_session"
OUTPUT_DIR = "./bill_texts"

# User-Agent rotation (optional)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
]

def create_or_use_persistent_session():
    """
    Create or reuse a persistent browser session to handle Cloudflare protections.
    """
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,  # Use False for manual CAPTCHA solving if required
            args=[
                f"--user-agent={random.choice(USER_AGENTS)}"  # Randomize User-Agent
            ]
        )
        page = browser.new_page()
        print("Persistent session created. Solve CAPTCHA if prompted.")
        input("Press Enter once you're logged in or CAPTCHA is solved...")
        browser.close()

def save_as_pdf(page, congress_url, bill_number):
    """
    Save the current page as a PDF.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_path = os.path.join(OUTPUT_DIR, f"{bill_number}.pdf")

    try:
        print(f"Navigating to {congress_url} for Bill Number {bill_number}")
        page.goto(congress_url)
        page.wait_for_load_state("load")

        # Save the page as a PDF
        page.pdf(path=output_path, format="A4", print_background=True)
        print(f"Saved PDF for Bill Number {bill_number} at {output_path}")
    except Exception as e:
        print(f"Error saving PDF for Bill Number {bill_number}: {e}")

def scrape_all_bill_texts(csv_filename="bills.csv"):
    """
    Read the Congress URLs from a CSV and save the pages as PDFs using a persistent session.
    """
    if not os.path.exists(SESSION_DIR):
        print(f"Session directory '{SESSION_DIR}' does not exist. Create it first.")
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=SESSION_DIR,
                headless=True,  # Switch to True for automated scraping
                args=[
                    f"--user-agent={random.choice(USER_AGENTS)}"  # Randomize User-Agent
                ]
            )
            page = browser.new_page()

            # Load the CSV
            with open(csv_filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    bill_number = row.get("Bill Number", "unknown").strip()
                    congress_url = row.get("Congress.gov URL", "").strip()
                    if not congress_url:
                        print(f"No URL provided for Bill Number {bill_number}")
                        continue
                    print(f"Processing Bill Number: {bill_number} from {congress_url}")
                    save_as_pdf(page, congress_url, bill_number)

                    # Add random delay to mimic human behavior
                    delay = random.uniform(3, 7)
                    print(f"Delaying for {delay:.2f} seconds...")
                    time.sleep(delay)

            browser.close()
    except Exception as e:
        print(f"Error during scraping: {e}")

if __name__ == "__main__":
    # Step 1: Create a persistent session (manual CAPTCHA handling)
    create_or_use_persistent_session()

    # Step 2: Reuse session to scrape bill texts
    scrape_all_bill_texts()
