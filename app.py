from flask import Flask, request, send_file, after_this_request
from PyPDF2 import PdfMerger
from PIL import Image
import os
import tempfile

app = Flask(__name__)

@app.route('/merge-pdf-api-2', methods=['POST'])
def merge_pdf():
    merger = PdfMerger()
    temp_files = []

    for file in request.files.getlist("files"):
        filename = file.filename.lower()
        temp_path = tempfile.mktemp(suffix=".pdf")

        if filename.endswith(".pdf"):
            file.save(temp_path)
        else:
            img = Image.open(file.stream).convert("RGB")
            img.save(temp_path, "PDF")

        merger.append(temp_path)
        temp_files.append(temp_path)

    output_pdf = tempfile.mktemp(suffix=".pdf")
    merger.write(output_pdf)
    merger.close()

    @after_this_request
    def cleanup(response):
        for f in temp_files:
            os.remove(f)
        os.remove(output_pdf)
        return response

    return send_file(output_pdf, as_attachment=True, download_name="merged.pdf")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

