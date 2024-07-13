import hashlib
import base64
import csv
import os

# Function to hash the account number
def hash_account_number(account_number):
    hashed = hashlib.sha256(account_number.encode()).digest()
    encoded = base64.b64encode(hashed)[:8]
    return encoded.decode()

# Function to encrypt the account number into a hashed format
def encrypt_account_number(account_number):
    hashed = hashlib.sha256(account_number.encode()).digest()
    encoded = base64.b64encode(hashed)[:8]
    return encoded.decode()

# Function to save account number and hash to a CSV file
def save_to_csv(account_number, hash_string):
    with open('encrypted_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([account_number, hash_string])

# Function to check if a hash exists in the CSV file
def check_hash_in_csv(hash_string):
    if os.path.exists('encrypted_data.csv'):
        with open('encrypted_data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == hash_string:
                    return True
    return False

# Function to decrypt a hash and get the original account number
def decrypt_hash(hash_string):
    if os.path.exists('encrypted_data.csv'):
        with open('encrypted_data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == hash_string:
                    return row[0]
    return None

# Main function
def main():
    while True:
        print("1. Encrypt an account number and save to CSV")
        print("2. Show stored encrypted account numbers")
        print("3. Decrypt a hash and show the original account number")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = input("Enter the account number to encrypt: ")
            hash_string = encrypt_account_number(account_number)
            save_to_csv(account_number, hash_string)
            print("Account number encrypted and saved successfully! Hash:", hash_string)

        elif choice == '2':
            if os.path.exists('encrypted_data.csv'):
                with open('encrypted_data.csv', 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    print("Stored encrypted account numbers:")
                    for row in reader:
                        print(f"Account Number: {row[0]}, Hash: {row[1]}")
            else:
                print("No encrypted account numbers found.")

        elif choice == '3':
            hash_string = input("Enter the hash to decrypt: ")
            account_number = decrypt_hash(hash_string)
            if account_number:
                print("Original account number:", account_number)
            else:
                print("Hash not found in the CSV file.")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
