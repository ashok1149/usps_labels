import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
import io

def create_image_pdf(address_image_path, temp_pdf_path, image_width, image_height, x_pos, y_pos, page_width, page_height):
    c = canvas.Canvas(temp_pdf_path, pagesize=(page_width, page_height))
    c.drawImage(address_image_path, x_pos, y_pos, width=image_width, height=image_height)
    c.save()

def insert_image_into_pdf(usps_label_pdf, address_image_path, output_pdf, image_width, image_height, x_pos, y_pos):
    reader = PdfReader(usps_label_pdf)
    first_page = reader.pages[0]
    page_width = float(first_page.mediabox[2])
    page_height = float(first_page.mediabox[3])

    temp_pdf_path = "temp_address_image.pdf"
    create_image_pdf(address_image_path, temp_pdf_path, image_width, image_height, x_pos, y_pos, page_width, page_height)

    image_pdf = PdfReader(temp_pdf_path)
    writer = PdfWriter()
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.merge_page(image_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf, 'wb') as f_out:
        writer.write(f_out)

# Specify the folder path containing the USPS labels and the output path
input_folder_path = r'E:\usps_labels'  # Folder containing USPS labels
output_folder_path = r'E:\usps output'  # Folder to save modified files
address_image_path = r'E:\usps images\address image.png'

# Image sizing and placement (values should be fine-tuned based on your label layout)
image_width = 125  
image_height = 38   
x_pos = 7          
y_pos = 270        

print(f"Processing files in: {input_folder_path}")

# Process each PDF file in the specified folder
for filename in os.listdir(input_folder_path):
    print(f"Found file: {filename}")  # Print each file found
    if filename.endswith('.pdf'):
        usps_label_pdf = os.path.join(input_folder_path, filename)
        output_pdf = os.path.join(output_folder_path, f'modified_{filename}')  # Save output in a different folder
        print(f"Processing: {usps_label_pdf} -> {output_pdf}")
        insert_image_into_pdf(usps_label_pdf, address_image_path, output_pdf, image_width, image_height, x_pos, y_pos)
        print(f"Output saved as: {output_pdf}")

print("Processing completed for all USPS labels in the folder.")
