# part 3 assignment - file handling, api and exception handling


# TASK 1 — FILE WRITE & READ


# writing initial notes to file so we can later read and test operations on it
with open("python_notes.txt", "w", encoding="utf-8") as f:
    f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
    f.write("Topic 2: Lists are ordered and mutable.\n")
    f.write("Topic 3: Dictionaries store key-value pairs.\n")
    f.write("Topic 4: Loops automate repetitive tasks.\n")
    f.write("Topic 5: Exception handling prevents crashes.\n")

print("File written successfully.")

# adding more content to same file instead of overwriting previous data
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help reuse code.\n")
    f.write("Topic 7: Python is easy to learn.\n")

print("Lines appended successfully.")


# reading file line by line and numbering it for better understanding
print("\nReading file content:")

line_count = 0

with open("python_notes.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"{i}. {line.strip()}")
        line_count += 1

print("Total lines:", line_count)


# taking user input to search a keyword in the file
keyword = input("\nEnter keyword to search: ").lower()

found = False

with open("python_notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        if keyword in line.lower():
            print(line.strip())
            found = True

if not found:
    print("No matching lines found.")



# TASK 2 — API INTEGRATION


import requests

url = "https://dummyjson.com/products?limit=20"

try:
    # calling api to fetch product data from internet
    response = requests.get(url, timeout=5)
    data = response.json()

    print("\nID | Title | Category | Price | Rating")

    for p in data["products"]:
        print(p["id"], "|", p["title"], "|", p["category"], "|", p["price"], "|", p["rating"])

    # filtering only high rated products to analyze better items
    high_rated = [p for p in data["products"] if p["rating"] >= 4.5]

    # sorting products so that highest price appears first
    high_rated.sort(key=lambda x: x["price"], reverse=True)

    print("\nFiltered Products (rating >= 4.5):")
    for p in high_rated:
        print(p["title"], p["price"], p["rating"])

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check internet.")
except requests.exceptions.Timeout:
    print("Request timed out.")
except Exception as e:
    print("Error:", e)


# fetching only laptops category to see category-based filtering
try:
    response = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
    data = response.json()

    print("\nLaptop Products:")
    for p in data["products"]:
        print(p["title"], p["price"])

except Exception as e:
    print("Error while fetching laptops:", e)


# sending dummy post request just to understand how data is sent to api
try:
    response = requests.post(
        "https://dummyjson.com/products/add",
        json={
            "title": "My Custom Product",
            "price": 999,
            "category": "electronics",
            "description": "Created via API"
        },
        timeout=5
    )

    print("\nPOST Response:")
    print(response.json())

except Exception as e:
    print("POST error:", e)



# TASK 3 — EXCEPTION HANDLING


# creating a safe division function to avoid program crash during errors
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nSafe divide tests:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# reading file safely using try-except so it doesn't crash if file is missing
def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

print("\nReading existing file:")
print(read_file_safe("python_notes.txt"))

print("\nReading missing file:")
read_file_safe("ghost_file.txt")


# taking user input and validating before calling api
while True:
    user_input = input("\nEnter product ID (1-100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Please enter a valid number.")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("Enter ID between 1 and 100.")
        continue

    try:
        res = requests.get(f"https://dummyjson.com/products/{pid}", timeout=5)

        if res.status_code == 404:
            print("Product not found.")
        else:
            data = res.json()
            print(data["title"], data["price"])

    except Exception as e:
        print("Error:", e)



# TASK 4 — ERROR LOGGING


from datetime import datetime

# creating a function to store errors in a file for tracking later
def log_error(context, error_type, message):
    with open("error_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] ERROR in {context}: {error_type} — {message}\n")


# forcing an error intentionally to test logging functionality
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error("fetch_products", "ConnectionError", str(e))


# simulating a 404 error to check if it gets logged properly
res = requests.get("https://dummyjson.com/products/999", timeout=5)

if res.status_code != 200:
    log_error("lookup_product", "HTTPError", f"Status {res.status_code}")


# reading log file to confirm errors are saved correctly
print("\nError Log Content:")
with open("error_log.txt", "r") as f:
    print(f.read())