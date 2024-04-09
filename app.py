from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'C:\\Users\\KAL-I\\Desktop\\New folder\\uploads')  # Use absolute path

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file uploaded')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')
    if file and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        pdf_path = convert_to_pdf(filepath)  # Pass full file path
        return render_template('result.html', pdf_path=pdf_path)
    else:
        return render_template('index.html', error='Invalid file format')

@app.route('/download/<filename>', methods=['GET'])
def download_pdf(filename):
    return send_file(filename, as_attachment=True)


def convert_to_pdf(image_path):
    pdf_path = os.path.splitext(image_path)[0] + '.pdf'
    img = Image.open(image_path)
    pdf = canvas.Canvas(pdf_path, pagesize=img.size)
    pdf.drawImage(image_path, 0, 0)
    pdf.save()
    return pdf_path

@app.route('/result/<pdf_path>')
def show_result(pdf_path):
    return render_template('result.html', pdf_path=pdf_path)


if __name__ == '__main__':
    app.run(debug=True)
