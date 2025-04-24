import fitz  # PyMuPDF
import os

def modify_pdf_text(usps_label_pdf, output_pdf, old_address, new_address):
    # Open the original PDF
    doc = fitz.open(usps_label_pdf)
    
    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        # Check if the old address exists and replace it
        if old_address in text:
            print(f"Found the address on page {page_num+1}. Replacing...")
            
            # Get the location of the old address on the page
            areas = page.search_for(old_address)
            
            # Redact the old address
            for area in areas:
                page.add_redact_annot(area, fill=(1, 1, 1))  # Adds a white box over old address
            page.apply_redactions()

            # Insert the new address at the position of the old one
            for area in areas:
                x0, y0, x1, y1 = area
                page.insert_text((x0, y0), new_address, fontsize=10)  # Customize font size, etc.

    # Save the modified PDF to the output file
    doc.save(output_pdf)
    doc.close()
    print(f"Output saved as: {output_pdf}")

# Specify the folder path containing the USPS labels and the output path
input_folder_path = r'E:\usps_labels'  # Folder containing USPS labels
output_folder_path = r'E:\usps output'  # Folder to save modified files

# Define the old and new addresses
old_address = "Jacky, 1325 REMINGTON,BLVD.UNIT B, 60490"
new_address = "TRENDIA, 1650 Premium Outlets Blvd, Unit 225, Aurora, IL 60502"

print(f"Processing files in: {input_folder_path}")

# Process each PDF file in the specified folder
for filename in os.listdir(input_folder_path):
    print(f"Found file: {filename}")  # Print each file found
    if filename.endswith('.pdf'):
        usps_label_pdf = os.path.join(input_folder_path, filename)
        output_pdf = os.path.join(output_folder_path, f'modified_{filename}')  # Save output in a different folder
        print(f"Processing: {usps_label_pdf} -> {output_pdf}")
        
        # Modify the address in the PDF
        modify_pdf_text(usps_label_pdf, output_pdf, old_address, new_address)
        print(f"Output saved as: {output_pdf}")

print("Processing completed for all USPS labels in the folder.")
