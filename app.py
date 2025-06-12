from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from supabase import create_client, Client

# Initialize Flask and Supabase
app = Flask(__name__)
CORS(app)

# Supabase configuration
supabase_url = "https://vhljluxzxhoxsrskolru.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZobGpsdXh6eGhveHNyc2tvbHJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkyNzYwMDUsImV4cCI6MjA2NDg1MjAwNX0.F0OJbpeKbIgIXIowSYQyA302IKJpe8NY6E9OP7VYSJE"
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/upload', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Load Excel file into a pandas DataFrame
        df = pd.read_excel(file)
        task_names = df['Task Name'].tolist()  # Extract 'Task Name' column

        # Save extracted data to Supabase (if needed)
        data = [{'title': task} for task in task_names]
        supabase.table('tasks').insert(data).execute()

        return jsonify({'task_names': task_names}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
