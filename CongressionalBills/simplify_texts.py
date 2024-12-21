import os
import PyPDF2
import openai
from dotenv import load_dotenv
import csv

# Load environment variables (e.g., OpenAI API key)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Debugging the loaded key
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
else:
    print(f"OPENAI_API_KEY loaded: {openai_api_key[:5]}***")  # Print partial key for security

# Set OpenAI API key
openai.api_key = openai_api_key

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

def simplify_text_with_ai(text):
    """
    Simplify the given text using OpenAI GPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal expert simplifying legal text into plain language."},
                {"role": "user", "content": f"Please simplify the following text:\n{text}"}
            ]
        )
        simplified_text = response["choices"][0]["message"]["content"]
        return simplified_text
    except Exception as e:
        print(f"Error simplifying text: {e}")
        return None

def process_pdfs_for_simplification(input_dir="bill_texts", output_csv="simplified_bills.csv"):
    """
    Process all PDFs in the input directory, extract text, simplify it, and save to CSV.
    """
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Bill Number", "Simplified Text"])

        for pdf_file in os.listdir(input_dir):
            if pdf_file.endswith(".pdf"):
                bill_number = os.path.splitext(pdf_file)[0]
                pdf_path = os.path.join(input_dir, pdf_file)

                print(f"Processing {pdf_path} for Bill Number {bill_number}")
                text = extract_text_from_pdf(pdf_path)
                if text:
                    simplified_text = simplify_text_with_ai(text)
                    writer.writerow([bill_number, simplified_text])
                    print(f"Simplified text for {bill_number} written to CSV.")
                else:
                    print(f"Failed to extract text from {pdf_path}.")

if __name__ == "__main__":
    process_pdfs_for_simplification()
