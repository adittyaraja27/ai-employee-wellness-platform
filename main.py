from ingestion.text_ingestion import (
    read_text_input,
    read_txt_file,
    read_csv_file,
    validate_text
)


# 1. Normal text
text = read_text_input("I am feeling stressed.")

if validate_text(text):
    print("1. Normal text: VALID")
else:
    print("1. Normal text: INVALID")


# 2. Empty text
text = read_text_input("")

if validate_text(text):
    print("2. Empty text: VALID")
else:
    print("2. Empty text: INVALID")


# 3. Spaces only
text = read_text_input("     ")

if validate_text(text):
    print("3. Spaces only: VALID")
else:
    print("3. Spaces only: INVALID")


# 4. None
text = read_text_input(None)

if validate_text(text):
    print("4. None: VALID")
else:
    print("4. None: INVALID")


# 5. CSV
try:
    texts = read_csv_file("data/sample.csv")
    print("5. CSV: VALID")
    print(texts)

except Exception as e:
    print("5. CSV: INVALID")
    print(e)

# 6. TXT test
try:
    text = read_txt_file("data/sample.txt")

    if validate_text(text):
        print("6. TXT: VALID")
        print(text)
    else:
        print("6. TXT: INVALID")

except Exception as e:
    print("6. TXT ERROR:", e)


# 7. Empty TXT test
try:
    text = read_txt_file("data/empty.txt")

    if validate_text(text):
        print("7. Empty TXT: VALID")
    else:
        print("7. Empty TXT: INVALID")

except Exception as e:
    print("7. Empty TXT ERROR:", e)

# 8. Invalid CSV test

try:
    texts=read_csv_file("data/invalid.csv")
    print("8. Invalid CSV: VALID")

except Exception as e:
    print("8. Invalid CSV: INVALID")
    print("ERROR:",e)

#9. Wrong file format test 

try:
    text = read_txt_file("data/sample.csv")
    print("9. Wrong format: ACCEPTED")

except Exception as e:
    print("9. wrong format: REJECTED")
    print("error:",e)

# 10. Wrong format: REJECTED
# Error: Only .csv files are supported

try:
    texts=read_csv_file("data/sample.txt")
    print("10. Wrong format: ACCEPTED")
except Exception as e:
    print("10. Wrong format: REJECTED")
    print("ERROR: ", e)


from preprocessing.text_preprocessor import preprocess_text

text = "I am REALLY stressed!!! I've been working continuously for 3 days."

processed = preprocess_text(text)

print("Original:")
print(text)

print("\nProcessed:")
print(processed)