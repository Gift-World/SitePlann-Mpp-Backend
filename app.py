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


    # updated code
@app.route('/upload', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Get project_id from the request form
    project_id = request.form.get('project_id')
    if not project_id:
        return jsonify({'error': 'project_id is required'}), 400

    try:
        # Load Excel file into a pandas DataFrame
        df = pd.read_excel(file)

        # Check required columns exist
        required_columns = ['Task Name', 'Status', 'Priority', 'Due Date']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'error': f'Missing column: {col}'}), 400

        # Convert rows into a list of dictionaries for Supabase
        data = []
        for _, row in df.iterrows():
            data.append({
                'title': row['Task Name'],
                'status': row['Status'],
                'priority': row['Priority'],
                'dueDate': row['Due Date'].isoformat() if not pd.isna(row['Due Date']) else None,
                'project_id': project_id  # Attach the project_id here
            })

        # Save data to Supabase
        supabase.table('tasks').insert(data).execute()

        return jsonify({'message': 'Tasks uploaded successfully', 'rows_uploaded': len(data)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

if __name__ == '__main__':
    app.run(debug=True)
