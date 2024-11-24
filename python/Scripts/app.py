from flask import Flask, request, jsonify
from flask_cors import CORS  # Import for CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for the app

@app.route('/start-scan', methods=['POST'])
def start_scan():
    # Get the URL from the POST request
    data = request.get_json()
    target_url = data.get('url', None)  # Ensure the URL is passed in the JSON payload

    if not target_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    # Set the URL in an environment variable for your scanning script to access
    os.environ['TARGET_URL'] = target_url

    try:
        # Define the location of the results file
        result_file = '../../front/src/data/results.json'

        # Ensure the result file is deleted before running the scan
        if os.path.exists(result_file):
            os.remove(result_file)

        # Log the current working directory
        print(f"Current working directory: {os.getcwd()}")

        # Run the vulnerability scanning script (e.g., vulnerabilities.py)
        print(f"Starting vulnerability scan for {target_url}...")

        # Ensure the correct path to vulnerabilities.py file
        result = subprocess.run(
        ['python', 'vulnerabilities.py'],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, 'TARGET_URL': target_url},
        )


        # Capture and print the output and error from the script
        print(f"Scan output: {result.stdout.decode()}")
        print(f"Scan error: {result.stderr.decode()}")

        # After scan completes, check if results.json exists
        if not os.path.exists(result_file):
            return jsonify({"status": "error", "message": "Scan results file not found"}), 500

        # Load the results and return them to the frontend
        with open(result_file, 'r') as f:
            results = json.load(f)

        return jsonify({"status": "success", "results": results})

    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        print(f"Error during scan: {e}")
        print(f"Error stdout: {e.stdout.decode()}")
        print(f"Error stderr: {e.stderr.decode()}")
        return jsonify({"status": "error", "message": f"Error during scan: {str(e)}"}), 500

    except Exception as e:
        # Capture and print any unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ensure Flask runs on port 5000 (or use 8080 if you prefer)
