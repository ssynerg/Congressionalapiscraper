# run_all.py
import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{script_name} completed successfully.\n")
    else:
        print(f"Error running {script_name}: {result.stderr}\n")

def convert_to_pdf_url(congress_url):
    """
    Convert a Congress.gov text URL to the corresponding PDF download URL.
    """
    try:
        parts = congress_url.split('/')
        congress_number = parts[4]
        bill_type = parts[5]
        bill_number = parts[6].split('-')[-1]
        pdf_url = f"https://www.congress.gov/{congress_number}/bills/{bill_type}{bill_number}/BILLS-{congress_number}{bill_type}{bill_number}ih.pdf"
        return pdf_url
    except Exception as e:
        print(f"Error converting to PDF URL: {e}")
        return None

if __name__ == "__main__":
    scripts = [
        "fetch_bills.py",  # Fetch bills and save to CSV
        "scrape_bill_texts.py",  # Scrape full texts from Congress URLs
        "simplify_texts.py",  # Simplify the bill texts
        "export_to_csv.py"  # Export simplified texts to final CSV
    ]

    for script in scripts:
        run_script(script)
