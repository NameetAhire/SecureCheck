from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import requests
import io
import time
import json
import os # Import os for path handling

# Set the template folder explicitly relative to the script location
# Since the static files are served from '.', we need to ensure Flask looks in 'templates'
# for render_template calls.
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

# --- Routes using send_from_directory (User's requirement) ---

# Note: These files must be in the project root directory alongside app.py
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/about')
def about():
    return send_from_directory('.', 'about.html')

@app.route('/contact')
def contact():
    return send_from_directory('.', 'contact.html')

@app.route('/breached_email.csv')
def serve_csv():
    return send_from_directory('.', 'breached_email.csv')

@app.route('/visualisation')
def visualisation():
    return send_from_directory('.', 'visualisation.html')

# --- API Route (Using render_template for dynamic results) ---

@app.route('/api', methods=['GET', 'POST'])
def api_page():
    results = []
    error = None

    if request.method == 'POST':
        uploaded_file = request.files.get('csv_file')
        
        # Check if the file is present and has the correct extension
        if uploaded_file and uploaded_file.filename.endswith('.csv'):
            try:
                # Read the file content into a string buffer
                stream = io.StringIO(uploaded_file.stream.read().decode("UTF8"))
                
                # Read CSV into pandas, assuming emails are in the first column (header=None)
                df = pd.read_csv(stream, header=None)
                
                # Ensure the first column exists and convert it to a list of strings
                if 0 in df.columns:
                    emails = df[0].astype(str).tolist()
                else:
                    error = "CSV file is empty or formatted incorrectly (expected emails in the first column)."
                    emails = []

            except Exception as e:
                error = f"Error reading CSV file: {str(e)}"
                emails = []

            if not error:
                for email in emails:
                    email = email.strip()
                    if not email:
                        continue

                    try:
                        # API Request setup
                        response = requests.get(
                            "https://leakcheck.net/api/public",
                            params={"check": email},
                            timeout=10
                        )
                        
                        # Raise an exception for bad status codes (4xx or 5xx)
                        response.raise_for_status() 
                        data = response.json()
                        
                        # --- FIX: Use 'sources' key instead of 'breaches' ---
                        sources = data.get("sources", [])
                        found = data.get("found", 0)
                        
                        # Set default status and styling
                        status = "⚠️ Unknown Status"
                        status_icon = "❓"
                        status_class = "bg-gray-400"
                        
                        num_breaches = 0
                        
                        # Logic to determine status, icon, class, and breach count
                        if found is None or found == 0:
                            status = "Safe — No breaches found!"
                            status_icon = "✅"
                            status_class = "bg-green-500"
                            num_breaches = 0
                            sources = [] # Ensure sources is empty if not found
                        else:
                            # Use the length of the 'sources' list, which is more reliable
                            if isinstance(sources, list):
                                num_breaches = len(sources)
                            elif isinstance(found, int):
                                # Fallback if sources is not a list, use the 'found' count
                                num_breaches = found 

                            status = f"Breached — {num_breaches} breach(es)"
                            status_icon = "❌"
                            status_class = "bg-red-500"

                        results.append({
                            "email": email, 
                            "status": status, 
                            "status_icon": status_icon,
                            "status_class": status_class,
                            "breaches": sources # Pass the list of source objects
                        })

                    except requests.exceptions.RequestException as req_e:
                        status = f"API Error: {req_e}"
                        results.append({"email": email, "status": status, "status_icon": "⚠️", "status_class": "bg-yellow-500", "breaches": []})
                    except Exception as e:
                        status = f"Processing Error: {str(e)}"
                        results.append({"email": email, "status": status, "status_icon": "⚠️", "status_class": "bg-yellow-500", "breaches": []})

                    # Time delay to comply with potential API rate limits
                    time.sleep(1) 
        
        else:
            error = "Please upload a valid CSV file."

    return render_template('api.html', results=results, error=error)
    
if __name__ == '__main__':
    # Use a dynamic port for hosting flexibility
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)