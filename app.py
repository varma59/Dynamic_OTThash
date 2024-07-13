from flask import Flask, request, jsonify, send_from_directory, render_template_string
import hashlib
import base64
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Function to hash the account number with a timestamp
def hash_account_number(account_number):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    unique_string = account_number + current_time
    hashed = hashlib.sha256(unique_string.encode()).digest()
    encoded = base64.b64encode(hashed)[:8]
    return encoded.decode(), current_time

# Function to save account number, hash, and timestamp to a CSV file
def save_to_csv(account_number, hash_string, timestamp):
    with open('encrypted_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([account_number, hash_string, timestamp])

@app.route('/secret-key', methods=['GET'])
def generate_secret_key():
    account_number = request.args.get('accountNumber')
    if account_number:
        hash_string, timestamp = hash_account_number(account_number)
        save_to_csv(account_number, hash_string, timestamp)
        return hash_string
    return "No account number provided", 400

@app.route('/')
def serve_index():
    return send_from_directory(app.root_path, 'index.html')

@app.route('/view-data')
def view_data():
    if os.path.exists('encrypted_data.csv'):
        with open('encrypted_data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = [row for row in reader]
    else:
        data = []

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Decrypted Data</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            h2 {
                text-align: center;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f4f4f4;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Decrypted Data</h2>
            <table>
                <tr>
                    <th>Account Number</th>
                    <th>Hash</th>
                    <th>Timestamp</th>
                </tr>
                {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data)

if __name__ == "__main__":
    app.run(debug=True)
