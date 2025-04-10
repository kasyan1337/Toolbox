import os
import sys
import shutil
import ocrmypdf


def ocr_pdfs(input_folder, output_folder, archive_folder, language='eng'):
    """
    Process PDF files in the input folder using OCR and save them to the output folder.

    Parameters:
        input_folder (str): Folder containing input PDF files.
        output_folder (str): Folder to save processed PDF files.
        archive_folder (str): Folder to archive processed/skipped files.
        language (str): Language(s) for OCR. Default is 'eng' (English).
                       Combine languages using a '+' (e.g., 'eng+rus').
    """
    # Ensure necessary folders exist
    for folder in [input_folder, output_folder, archive_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    archive_input = os.path.join(archive_folder, 'input')
    archive_output = os.path.join(archive_folder, 'output')
    os.makedirs(archive_input, exist_ok=True)
    os.makedirs(archive_output, exist_ok=True)

    # List all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'.")
        return

    for pdf_file in pdf_files:
        input_path = os.path.join(input_folder, pdf_file)
        output_path = os.path.join(output_folder, pdf_file)
        archive_input_path = os.path.join(archive_input, pdf_file)
        archive_output_path = os.path.join(archive_output, pdf_file)

        # Skip processing if the output file already exists
        if os.path.exists(output_path):
            print(f"Skipping '{pdf_file}' - already processed.")
            shutil.move(input_path, archive_input_path)
            shutil.move(output_path, archive_output_path)
            print(f"Moved '{pdf_file}' to archive.")
            continue

        print(f"Processing '{pdf_file}'...")

        try:
            ocrmypdf.ocr(
                input_file=input_path,
                output_file=output_path,
                language=language,
                deskew=True,
                force_ocr=True,  # Force OCR even if the PDF has searchable text
                progress_bar=True
            )
            print(f"Saved OCR'd PDF to '{output_path}'.")
        except Exception as e:
            print(f"Failed to OCR '{pdf_file}': {e}")


if __name__ == "__main__":
    # Define the main folders
    source_folder = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(source_folder, 'input')
    output_folder = os.path.join(source_folder, 'output')
    archive_folder = os.path.join(source_folder, 'archive')

    # Language documentation
    """
    Available Tesseract language codes:
    - English: 'eng'
    - Slovak: 'slk'
    - Czech: 'ces'
    - Russian: 'rus'
    - Chinese Simplified: 'chi_sim'
    - Chinese Traditional: 'chi_tra'
    - Polish: 'pol'
    - German: 'deu'
    - French: 'fra'
    - Finnish: 'fin'

    Combine multiple languages using a '+' (e.g., 'eng+rus').
    """

    # Set the language for OCR (default to English)
    language = 'fin'

    # Allow passing the language as a command-line argument
    if len(sys.argv) > 1:
        language = sys.argv[1]  # e.g., python main.py eng+rus

    # Call the OCR function
    ocr_pdfs(input_folder, output_folder, archive_folder, language)