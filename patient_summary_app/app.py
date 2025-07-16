import os
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
RESULTS_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Extraction prompt for o3-mini API
EXTRACTION_PROMPT = '''\
Generate a longitudinal cognitive summary in the following format using both structured data (codes, medications, vital signs, laboratory results) and unstructured data (clinical notes, discharge summaries). If no information is found, state 'Not documented'.

Risk factors for dementia
- Education level: Any mentions? If yes, provide short summary and date(s).
- Hearing loss: Any mentions? If yes, provide short summary and date(s).
- Vision loss: Any mentions? If yes, provide short summary and date(s).
- High cholesterol: Any mentions? If yes, provide short summary and date(s).
- Depression: Any mentions? If yes, provide short summary and date(s).
- Traumatic brain injury: Any mentions? If yes, provide short summary and date(s).
- Physical inactivity: Any mentions? If yes, provide short summary and date(s).
- Diabetes: Any mentions? If yes, provide short summary and date(s).
- Smoking: Any mentions? If yes, provide short summary and date(s).
- Hypertension: Any mentions? If yes, provide short summary and date(s).
- Obesity: Any mentions? If yes, provide short summary and date(s).
- Excess alcohol use: Any mentions? If yes, provide short summary and date(s).
- Social isolation: Any mentions? If yes, provide short summary and date(s).
- Exposure to air pollution: Any mentions? If yes, provide short summary and date(s).

Cognitive assessment
- Cognitive tests performed: Montreal Cognitive Assessment (MoCA), Mini-Mental State Examination (MSSE), Addenbrooke's Cognitive Examination (ACE, ACE-III), Rowland Universal Dementia Assessment Scale (RUDAS)
- Most recent score and date
- Previous scores and date
- Neuropsychology assessment performed previously: Yes/No
  o If yes, state the date, indication for assessment, and summarisation of findings.

Service utilisation
- Geriatrician reviews: Yes/No. If yes, list the dates.
- Neurologist reviews: Yes/No. If yes, list the dates.
- Memory/dementia/CDAMS clinics: Yes/No. If yes, list the dates.
- Referrals to memory/dementia/CDAMS clinics: Yes/No. If yes, list the dates.

Medications
- Dementia/delirium related
  o Antipsychotics (quetiapine, risperidone, haloperidol, droperidol, olanzapine): Yes/No. If yes, date of prescription.
  o Cholinesterase inhibitors (donepezil, rivastigmine etc): Yes/No. If yes, date of prescription.
- Related to dementia risk factors:
  o Antihypertensives (ACE inhibitors, thiazides, beta blockers): Yes/No. If yes, date of prescription.
  o Cholesterol drugs (statins, ezetimibe): Yes/No. If yes, date of prescription.
  o Diabetes medications: Yes/No
- Medications that contribute to confusion
  o Benzodiazepines (diazepam, clonazepam etc): Yes/No. If yes, date of prescription.
  o Anticholinergics: Yes/No. If yes, date of prescription.

Diagnoses
- Delirium: Yes/No. If yes, date of diagnostic code or mention.
- Dementia (Alzheimer's disease, vascular dementia, frontotemporal dementia, mixed dementia): Yes/No. If yes, date of diagnostic code or mention.
- Mild cognitive impairment (MCI): Yes/No. If yes, date of diagnostic code or mention.
- Depression: Yes/No. If yes, date of diagnostic code or mention.
- Anxiety: Yes/No. If yes, date of diagnostic code or mention.

Relevant concepts from notes
- Confusion, agitation, aggression
- Code grey
- BPSD (eg, wandering, calling out, hallucinations)
- Functional decline
- Memory concerns/cognitive decline
- Carer concerns
- Mood disorders
'''

# Placeholder for o3-mini API call 1: CSV to natural language
def csv_to_natural_language(csv_path: str) -> str:
    # TODO: Replace with actual o3-mini API call
    df = pd.read_csv(csv_path)
    return df.to_string()

# Placeholder for o3-mini API call 2: Extract info from natural language
def extract_information(natural_text: str) -> dict:
    # TODO: Replace with actual o3-mini API call and extraction logic
    # This is where you would send both the natural_text and EXTRACTION_PROMPT to o3-mini
    # For now, return dummy data for all required fields
    return {
        "Education level": "Not documented",
        "Hearing loss": "Not documented",
        "Vision loss": "Not documented",
        "High cholesterol": "Not documented",
        "Depression": "Not documented",
        "Traumatic brain injury": "Not documented",
        "Physical inactivity": "Not documented",
        "Diabetes": "Not documented",
        "Smoking": "Not documented",
        "Hypertension": "Not documented",
        "Obesity": "Not documented",
        "Excess alcohol use": "Not documented",
        "Social isolation": "Not documented",
        "Exposure to air pollution": "Not documented",
        "Cognitive tests performed": "Not documented",
        "Most recent score and date": "Not documented",
        "Previous scores and date": "Not documented",
        "Neuropsychology assessment performed previously": "Not documented",
        "Geriatrician reviews": "Not documented",
        "Neurologist reviews": "Not documented",
        "Memory/dementia/CDAMS clinics": "Not documented",
        "Referrals to memory/dementia/CDAMS clinics": "Not documented",
        "Antipsychotics": "Not documented",
        "Cholinesterase inhibitors": "Not documented",
        "Antihypertensives": "Not documented",
        "Cholesterol drugs": "Not documented",
        "Diabetes medications": "Not documented",
        "Benzodiazepines": "Not documented",
        "Anticholinergics": "Not documented",
        "Delirium": "Not documented",
        "Dementia": "Not documented",
        "Mild cognitive impairment (MCI)": "Not documented",
        "Depression diagnosis": "Not documented",
        "Anxiety": "Not documented",
        "Confusion, agitation, aggression": "Not documented",
        "Code grey": "Not documented",
        "BPSD": "Not documented",
        "Functional decline": "Not documented",
        "Memory concerns/cognitive decline": "Not documented",
        "Carer concerns": "Not documented",
        "Mood disorders": "Not documented"
    }

# Format extracted info as markdown
def format_markdown(info: dict) -> str:
    return '\n'.join([f'**{k}**: {v}' for k, v in info.items()])

@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
def handle_upload(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    # Step 1: CSV to natural language
    natural_text = csv_to_natural_language(file_location)
    # Step 2: Extract information
    info = extract_information(natural_text)
    # Step 3: Format as markdown
    markdown = format_markdown(info)
    # Save markdown to file
    md_filename = file.filename + ".md"
    md_path = os.path.join(RESULTS_DIR, md_filename)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    return templates.TemplateResponse("result.html", {"request": request, "markdown": markdown, "md_filename": md_filename})

@app.get("/download/{md_filename}")
def download_markdown(md_filename: str):
    md_path = os.path.join(RESULTS_DIR, md_filename)
    return FileResponse(md_path, media_type="text/markdown", filename=md_filename)

app.mount("/static", StaticFiles(directory="static"), name="static") 