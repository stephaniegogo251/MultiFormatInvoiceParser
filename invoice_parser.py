#importing necessary libraries
import pytesseract
import pdfplumber
import re
import json
from PIL import Image
import tkinter as tk
import os
from tkinter import filedialog

#define dictionary to store invoice data
invoice_data = {}

#funtion to open file dialog and select a file to extract text from
def open_file():
    filepath = filedialog.askopenfilename(initialdir="D:\\Download", title="Select a File",
                                            filetypes=(("PDF files", "*.pdf"), ("Image files", "*.jpg;*.png")))
    extension = os.path.splitext(filepath)[1].lower()
    if extension == '.pdf':
        extract_text_from_pdf(filepath)
    elif extension in ['.jpg', '.png']:
        extract_text_from_image(filepath)
    else:
        print("Unsupported file type. Please select a PDF or image file.")

#function to extract text from PDF file using pdfplumber
def extract_text_from_pdf(filepath):
    with pdfplumber.open(filepath) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        extract_invoice_data(text)

#function to extract text from image file using pytesseract
def extract_text_from_image(filepath):
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)
    extract_invoice_data(text)

#function to extract invoice data using regular expressions (according to the invoice format)
def extract_invoice_data(text):
    invoice_number = re.search(r'(?:#\s*I\s*N\s*V|Invoice\s*)(?:Number|No|#)?\s*[-:]\s*(\d+)', text, re.IGNORECASE)
    vendor_name  = re.search(r'(?:Vendor|Issued To|Billed To|From|Supplier|Bill\s*To|Invoice\s*To)(?:[\s*\n*]?)(?:[:\-]?)(?:[\s*\n*]?)(.+?)\s*\n*?(?=[\n*\s*]([0-9]|Send|hello|Pay To|Invoice|Date|Address|Balance))', text, re.IGNORECASE | re.DOTALL)
    amount = re.search(r'(?:\w[:\-])?\s*(?:Amount\s*Due|Balance\s*Due|Total\s*Due|Invoice\s*Total|(?<!Sub)Total\s*)(?:[:\-])?\s*(\$\s*[\d,]+(?:\.\d{2})?)', text, re.IGNORECASE)
    
    if invoice_number:
        invoice_data['Invoice Number'] = invoice_number.group(1)
    else:
        invoice_data['Invoice Number'] = 'Not found'
    if vendor_name:
        invoice_data['Vendor Name'] = vendor_name.group(1)
    else:
        invoice_data['Vendor Name'] = 'Not found'
    if amount:
        invoice_data['Amount'] = amount.group(1)
    else:
        invoice_data['Amount'] = 'Not found'

    #Display the extracted data in the GUI
    button.destroy()
    label2.config(bg="lavender", text=f"Invoice Number: {invoice_data['Invoice Number']}")
    label2.pack(pady=10)
    label3 = tk.Label(root, text=f"Vendor Name: {invoice_data['Vendor Name']}", bg="lavender", font=("Arial", 16))
    label3.pack(pady=10)
    label4 = tk.Label(root, text=f"Amount: {invoice_data['Amount']}", bg="lavender", font=("Arial", 16))
    label4.pack(pady=10)
    button2 = tk.Button(root, text="Save Data", command=create_file)
    button2.config(bg="purple", fg="white", font=("Arial", 12))
    button2.pack(pady=10)

#function to create a JSON file and save the extracted data
def create_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filepath != "":
        file = open(filepath, "w")
        data = json.dumps(invoice_data, indent=4)
        file.write(data)
        file.close()
    print("Data saved successfully!")
    root.destroy()

#function to create the GUI using tkinter
root = tk.Tk()
root.title("Invoice Parser")
root.geometry("400x300")
root.configure(bg="lavender")
root.iconbitmap("icon.ico")

label1 = tk.Label(root, text="Invoice Parser", font=("Arial", 20), bg="lavender")
label1.pack(pady=10)

label2 = tk.Label(root, text="Select a PDF or Image file", bg="lavender", font=("Arial", 16))
label2.pack(pady=20)

label3 = tk.Label(root, text="", bg="lavender", font=("Arial", 16))
label3.pack(pady=10)

label4 = tk.Label(root, text="", bg="lavender", font=("Arial", 16))
label4.pack(pady=10)

button = tk.Button(root, text="Open File", command=open_file)
button.config(bg="purple", fg="white", font=("Arial", 12))
button.pack(pady=10)

#function to run the GUI
root.mainloop()