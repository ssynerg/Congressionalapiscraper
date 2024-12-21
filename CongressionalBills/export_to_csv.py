# export_to_csv.py
import csv
import os

def export_to_csv(input_dir='simplified_texts', output_filename='simplified_bills.csv'):
    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Bill ID', 'Simplified Text'])
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                bill_id = filename.replace('.txt', '')
                with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as text_file:
                    simplified_text = text_file.read()
                writer.writerow([bill_id, simplified_text])
                print(f'Exported: {bill_id}')

if __name__ == "__main__":
    export_to_csv()
