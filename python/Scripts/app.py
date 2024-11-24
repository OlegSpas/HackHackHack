import json
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/start-scan', methods=['POST'])
def start_scan():
    data = request.get_json()
    target_url = data.get('url', 'http://localhost:8000')  # Default target URL

    # Run the scanning script and collect results
    try:
        result_file = 'results.json'
        os.environ['TARGET_URL'] = target_url
        subprocess.run(['python', 'vulnerability_scanner.py'], check=True)  # Replace with your script name

        # Read the results from the JSON file
        with open(result_file, 'r') as f:
            results = json.load(f)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
