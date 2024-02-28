import pdfplumber

# Initialize an empty list to store road segment data
road_segments = []

# Print the column headers
print("kkno,dilimno,uzunluk,tasit,hiz")

# Open the PDF file
with pdfplumber.open("22TrafikUlasimBilgileri.pdf") as pdf:
    # Iterate over each page in the PDF
    for page in pdf.pages:
        # Extract tables from the page
        tables = page.extract_tables()
        # Iterate over each table
        for table in tables:
            # Check if the table has more than one row and the first cell of the second row is 'BL.\nNO'
            if len(table) > 1 and len(table[1]) > 0 and table[1][0] == 'BL.\nNO':
                # Iterate over each row starting from the third row
                for row in table[2:]:
                    # Extract data from the row
                    kkno = (row[2] or "").strip()
                    dilimno = (row[3] or "").strip()
                    uzunluk = (row[4] or "").strip()
                    tasit = (row[6] or "").strip()
                    hiz = (row[8] or "").strip()
                    # Append the data to the list
                    road_segments.append({
                        "kkno": kkno,
                        "dilimno": dilimno,
                        "uzunluk": uzunluk,
                        "tasit": tasit,
                        "hiz": hiz
                    })
                    # Print the data
                    print(f"{kkno},{dilimno},{uzunluk},{tasit},{hiz}")