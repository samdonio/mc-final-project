import pandas as pd
import requests
import json

# Define the function to load CSV, convert to JSON, and send POST request
def send_csv_as_json(csv_file_path, url):
    # Load CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Rename columns
    df = df.rename(columns={"x_pos": "x", "y_pos": "y", "z_pos": "z"})

    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records')
    
    # Wrap with "data" key
    wrapped_data = {
        "data": json.loads(json_data)
    }

    # Convert back to JSON string if needed
    wrapped_data = {
        "data": json.loads(json_data)
    }

    # Send POST request with JSON data
    response = requests.post(url, json=wrapped_data)
    
    # Print response status and text
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

if __name__ == "__main__":
    # Path to your CSV file
    
    # Endpoint URL
    url = 'http://127.0.0.1:5000/character'
    
    for i in range(26):
        csv_file_path = '../Data/Upsampled/' + chr(ord('A')+i) + '_01.csv'
        # Call the function to send CSV data as JSON
        send_csv_as_json(csv_file_path, url)
