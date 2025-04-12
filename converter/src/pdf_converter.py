import os
import platform
from subprocess import run

from pdf2docx import Converter

from converter.src.docx_cleaner import clean_up_docx

output_folder = "output"


def pdf_to_docx(input_path: str, output_path: str):
    # Ensure output file has a single .docx extension
    if not output_path.endswith(".docx"):
        output_path += ".docx"

    # Convert PDF to DOCX
    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()

    # Clean up the formatting in the generated DOCX file
    output_folder = os.path.dirname(output_path)
    clean_up_docx(output_path, output_folder)


def docx_to_pdf(input_path: str, output_path: str):
    if platform.system() == "Windows":
        # On Windows, use COM interface (as before)
        import comtypes.client
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(input_path)
        doc.SaveAs(output_path, FileFormat=17)  # 17 is the format ID for PDF
        doc.Close()
        word.Quit()
    elif platform.system() == "Darwin":  # macOS
        # Use LibreOffice for DOCX to PDF conversion on macOS
        command = [
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(output_path),
            input_path
        ]
        result = run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print("LibreOffice conversion failed:", result.stderr)
            return

        # Rename converted file to match expected output path
        converted_pdf = os.path.splitext(input_path)[0] + ".pdf"
        if os.path.exists(converted_pdf):
            os.rename(converted_pdf, output_path)
            print(f"Conversion to PDF completed: {output_path}")
        else:
            print("Error: PDF output not found after conversion.")
