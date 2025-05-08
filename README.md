This is a Python application that extracts data from an invoice—such as invoice number, vendor name, and total amount—from PDF or image files. Using pdfplumber and pytesseract, the app can read data from invoices,
then display the extracted data via a simple tkinter GUI. The user can choose a file, view the extracted information, and save it as a structured JSON file. The program uses regular expressions for basic invoice
structure matching and can be extended for more formats. Hence, the invoice parser cannot be used for all formats, but only for the ones it has been tested on.
