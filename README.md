This project automates the process of fetching and scraping bills and amendments from the U.S. Congress API and website. The tool saves the texts in user-friendly formats for further analysis. It is designed to enhance legislative transparency and accessibility.

---

## Features

- **Fetch Bills and Amendments**: Retrieves detailed information about bills and their amendments using the Congress API.
- **Scrape Bill and Amendment Texts**: Automates downloading of full texts of bills and amendments from Congress.gov.
- **Export to CSV**: Saves processed data for further analysis.

---

## Requirements

### Python Libraries
Install the required Python libraries using:

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `requests`: For API requests.
- `playwright`: For scraping Congress.gov.
- `dotenv`: For managing API keys securely.

### System Requirements
- Python 3.10 or newer
- Playwright dependencies:
  ```bash
  playwright install
  ```
- For Linux systems (Ubuntu):
  ```bash
  sudo apt install libx11-xcb1 libxcomposite1 libxi6 libxtst6 libnss3 libatk-bridge2.0-0 libgtk-3-0
  ```

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/congress-bills-scraper.git
cd congress-bills-scraper
```

### 2. Configure Environment Variables
Create a `.env` file with the following content:
```env
CONGRESS_API_KEY=your-congress-api-key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright
```bash
playwright install
```

---

## Usage

### 1. Fetch Bills and Amendments
Fetch bills and their associated amendments:
```bash
python fetch_bills.py
```
This generates a `bills_with_amendments.csv` containing:
- Bill details (e.g., title, number).
- Links to full texts and amendments.

### 2. Scrape Texts
Scrape full texts of bills and amendments:
```bash
python scrape_bill_texts.py
```
The texts are saved as PDFs or plain text in the `bill_texts/` and `amendments/` directories.

---

## File Structure

```
.
├── fetch_bills.py                # Fetches bills and amendments from the Congress API
├── scrape_bill_texts.py          # Scrapes full texts of bills and amendments
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (API keys)
├── bill_texts/                   # Directory for downloaded bill texts
├── amendments/                   # Directory for downloaded amendment texts
├── README.md                     # Project documentation
```

---

## Contribution

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments
- [Congress API](https://api.congress.gov/)
- [Playwright](https://playwright.dev/)
