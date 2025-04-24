import os
import re
import pdfplumber
from shutil import move

# Folder paths
input_folder = 'E:\china_sequence'  # Folder where your PDFs are stored
output_folder = 'E:\china_sequence_output'  # Folder where sorted PDFs will be moved

# Function to extract SKUs from the PDF file
def extract_skus(pdf_path):
    skus = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract the table from the page
            table = page.extract_table()
            if table:
                for row in table:
                    # Assuming SKU is in a specific column (e.g., column 0), adjust if needed
                    sku = row[0] if row else None
                    if sku:
                        skus.append(sku)
    return skus

# Function to sort SKUs numerically first, then alphabetically
def sort_skus(skus):
    # Define sorting function for numbers and letters
    def sort_key(x):
        # Extract numeric part and text part for sorting
        match = re.match(r'(\d+)([A-Za-z]*)', x)
        if match:
            return int(match.group(1)), match.group(2)
        return x
    
    return sorted(skus, key=sort_key)

# Function to rename and move the PDFs
def rename_and_move_pdf(pdf_path, skus, order_number):
    # Sort the SKUs
    sorted_skus = sort_skus(skus)
    
    # Handle file renaming
    if len(sorted_skus) == 1:
        new_name = f"{sorted_skus[0]}_{order_number}.pdf"
    else:
        new_name = f"multi*{len(sorted_skus)}_{order_number}.pdf"
    
    # Define the new path
    new_path = os.path.join(output_folder, new_name)
    
    # Move the file to the new folder
    move(pdf_path, new_path)
    print(f"Moved: {new_name}")

# Main function to process PDFs
def process_pdfs():
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            
            # Extract order number from filename (assuming it's in the format Order_1234.pdf, adjust if needed)
            order_number = re.search(r'Order_(\d+)', filename)
            if order_number:
                order_number = order_number.group(1)
            
            # Extract SKUs from the packing slip
            skus = extract_skus(pdf_path)
            
            if skus:
                # Rename and move the file
                rename_and_move_pdf(pdf_path, skus, order_number)

if __name__ == "__main__":
    process_pdfs()