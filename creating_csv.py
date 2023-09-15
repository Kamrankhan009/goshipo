import csv

# Sample address data with detailed information for "Address From" and "Address To"
address_pairs = [
    {
        "Address From": "123 Main St",
        "City From": "New York",
        "State From": "NY",
        "ZIP From": "10001",
        "Country from": "US",
        "Address To": "456 Elm St",
        "City To": "Los Angeles",
        "State To": "CA",
        "ZIP To": "90001",
        "Country to":"US"
    },
    {
        "Address From": "789 Oak St",
        "City From": "London",
        "State From": "",
        "ZIP From": "W1K 6TG",
        "Country from":"US",
        "Address To": "101 Pine St",
        "City To": "San Francisco",
        "State To": "CA",
        "ZIP To": "94101",
        "Country to":"US"
    },
    {
        "Address From": "555 Maple Ave",
        "City From": "Chicago",
        "State From": "IL",
        "ZIP From": "60601",
        "Country from":"US",
        "Address To": "777 Cedar Rd",
        "City To": "Miami",
        "State To": "FL",
        "ZIP To": "33101",
        "Country to":"US"
    },
]

# Define the CSV file name
csv_file = "detailed_address_pairs.csv"

# Write address pairs with detailed information to the CSV file
with open(csv_file, mode='w', newline='') as file:
    fieldnames = ["Address From", "City From", "State From", "ZIP From", "Country from", "Address To", "City To", "State To", "ZIP To", "Country to"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the address pairs
    for address_pair in address_pairs:
        writer.writerow(address_pair)

print(f"CSV file '{csv_file}' has been created with detailed address data for 'Address From' and 'Address To'.")
