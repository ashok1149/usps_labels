import os
import re
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm

input_folder = "E:\\sorting_input"
output_folder = "E:\\sorting_output"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith(".pdf"):
        continue

    input_pdf_path = os.path.join(input_folder, filename)
    output_pdf_path = os.path.join(output_folder, f"sorted_{filename}")

    reader = PdfReader(input_pdf_path)
    page_sku_pairs = []

    for i, page in tqdm(enumerate(reader.pages), total=len(reader.pages), desc=f"Processing {filename}"):
        text = page.extract_text()
        
        match = re.search(r"\b([A-Z0-9\-]{4,})[;*]", text or "")
        sku = match.group(1) if match else f"ZZZ{i:04}"

        page_sku_pairs.append((i, sku))

    sorted_pages = sorted(page_sku_pairs, key=lambda x: x[1])

    writer = PdfWriter()
    for index, _ in sorted_pages:
        writer.add_page(reader.pages[index])

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print(f"✅ Sorted PDF saved: {output_pdf_path}")
