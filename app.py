from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import pandas as pd
from supabase import create_client, Client

# Initialize Flask and Supabase
app = Flask(__name__)
CORS(app)

# Supabase configuration
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
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
    project_id = request.form.get('projectId')
    if not project_id:
        return jsonify({'error': 'project_id is required'}), 400
    
    print("Received projectId:", request.form.get("projectId"))
    
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
                'project_id': project_id
            })

        # Save data to Supabase
        supabase.table('tasks').insert(data).execute()

        return jsonify({'message': 'Tasks uploaded successfully', 'rows_uploaded': len(data)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

if __name__ == '__main__':
    app.run(debug=True)
