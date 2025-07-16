# Patient Summary App

A locally hosted web app for uploading patient CSV files, extracting longitudinal cognitive summaries using o3-mini APIs, and generating markdown reports.

## Features
- Upload CSV files with patient data
- Process data via o3-mini APIs
- Extract and display required information
- Download markdown summary

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `uvicorn main:app --reload`
3. Open your browser to `http://localhost:8000` 