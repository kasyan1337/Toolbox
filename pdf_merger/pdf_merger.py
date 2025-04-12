import os
from PyPDF2 import PdfMerger, PdfReader
from datetime import datetime

# Define directories
project_root = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(project_root, "input")
output_dir = os.path.join(project_root, "output")
archive_dir = os.path.join(project_root, "archive")

# Ensure necessary directories exist
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)
os.makedirs(os.path.join(archive_dir, "input"), exist_ok=True)
os.makedirs(os.path.join(archive_dir, "output"), exist_ok=True)


def validate_pdf(file_path):
    """
    Check if a file is a valid PDF.
    """
    try:
        PdfReader(file_path)
        return True
    except Exception:
        return False


def get_next_task_number(archive_subdir):
    """
    Determine the next task number based on existing files in the archive.
    """
    archive_target = os.path.join(archive_dir, archive_subdir)
    existing_files = os.listdir(archive_target)
    existing_numbers = [
        int(file.split(" - ")[0]) for file in existing_files if file.split(" - ")[0].isdigit()
    ]
    return max(existing_numbers, default=0) + 1


def get_file_order(file_list):
    """
    Get the custom order of files from the user.
    """
    print("Files found for merging:")
    for i, file_name in enumerate(file_list, start=1):
        print(f"{i}. {file_name}")

    while True:
        order_input = input("Enter the desired order of files (e.g., 3214): ")
        if all(char.isdigit() and 1 <= int(char) <= len(file_list) for char in order_input):
            order = [int(char) - 1 for char in order_input]
            return [file_list[i] for i in order]
        else:
            print("Invalid input. Please ensure you use numbers corresponding to the files listed above.")


def merge_pdfs(file_list, output_path):
    """
    Merge the given list of PDF files into a single PDF.
    """
    merger = PdfMerger()
    print("Merging files in the following order:")
    for file in file_list:
        print(f"- {file}")
        file_path = os.path.join(input_dir, file)
        if validate_pdf(file_path):
            with open(file_path, "rb") as pdf_file:
                merger.append(pdf_file)
        else:
            print(f"Skipping invalid PDF file: {file}")

    merger.write(output_path)
    merger.close()
    print(f"Files merged into: {output_path}")


def move_files_to_archive(source_dir, archive_subdir):
    """
    Move files from the source directory to the archive with task numbering and timestamp.
    """
    archive_target = os.path.join(archive_dir, archive_subdir)
    task_number = get_next_task_number(archive_subdir)
    timestamp = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

    for file_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file_name)

        # Validate that the file is a PDF
        if os.path.isfile(source_path) and file_name.lower().endswith(".pdf"):
            # Preserve the original file name
            base_name, ext = os.path.splitext(file_name)
            new_name = f"{str(task_number).zfill(4)} - {timestamp} - {base_name}{ext}"
            destination_path = os.path.join(archive_target, new_name)

            # Rename and move the file
            os.rename(source_path, destination_path)
            print(f"Moved {file_name} to {archive_target} as {new_name}")


def main():
    # Check if there are any existing output files
    if os.listdir(output_dir):
        print("Output directory is not empty. Archiving existing output files...")
        move_files_to_archive(output_dir, "output")

    # Get a list of input files
    input_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]

    if not input_files:
        print("No PDF files found in the input directory. Add files and try again.")
        return

    # Validate and filter input files
    input_files = [f for f in input_files if validate_pdf(os.path.join(input_dir, f))]

    if not input_files:
        print("No valid PDF files found in the input directory. Add valid files and try again.")
        return

    # Get custom file order from the user
    ordered_files = get_file_order(input_files)

    # Define the output file path
    output_file = os.path.join(output_dir, "Merged.pdf")

    # Merge the files
    merge_pdfs(ordered_files, output_file)

    # Move processed input files to the archive
    print("Archiving processed input files...")
    move_files_to_archive(input_dir, "input")

    print("Processing complete.")


if __name__ == "__main__":
    main()