import os
import pytesseract
from flask import Blueprint, render_template, request, redirect, flash, current_app
from werkzeug.utils import secure_filename
from PIL import Image
from pdf2image import convert_from_path

bp = Blueprint('upload_docs', __name__, url_prefix='/upload-doc')

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


@bp.route('/', methods=['GET', 'POST'])
def upload_doc():
    
    # If on Windows, set path to tesseract executable
    pytesseract.pytesseract.tesseract_cmd = current_app.config.get('TESSERACT_PATH', 'tesseract')
    
    if request.method == 'POST':
        file = request.files.get('document')
        doc_type = request.form.get('doc_type')

        if not file:
            flash("No file selected.")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            flash("Invalid file type.")
            return redirect(request.url)

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)

        text = extract_text(filepath, ext)

        # Try extract a date-like string
        detected_date = extract_date(text)

        flash(f"{doc_type.capitalize()} scanned successfully!")
        if detected_date:
            flash(f"🕒 Detected expiry or valid date: {detected_date}")
        else:
            flash("⚠️ Could not detect a valid date from the document.")

        return redirect(request.url)

    return render_template('upload_docs.html')

def extract_text(filepath, ext):
    if ext == 'pdf':
        pages = convert_from_path(filepath, 300)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        return text
    else:
        image = Image.open(filepath)
        return pytesseract.image_to_string(image)

import re
def extract_date(text):
    # Match common date formats like DD/MM/YYYY, YYYY-MM-DD, etc.
    patterns = [
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b(?:Expires|Valid until|Expiry)[:\s]*(\d{2}/\d{2}/\d{4})\b',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0)
    return None
