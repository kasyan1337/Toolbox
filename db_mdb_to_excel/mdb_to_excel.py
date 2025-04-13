import subprocess
import pandas as pd
import os
import glob
import io


def extract_tables(mdb_path: str, output_dir: str):
    result = subprocess.run(["mdb-tables", mdb_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error reading tables from {mdb_path}: {result.stderr}")
        return
    tables = result.stdout.strip().split()
    for table in tables:
        try:
            csv_data = subprocess.check_output(
                ["mdb-export", mdb_path, table], text=True
            )
            df = pd.read_csv(io.StringIO(csv_data))
            excel_file = os.path.join(output_dir, f"{table}.xlsx")
            df.to_excel(excel_file, index=False)
            print(f"Exported table '{table}' to {excel_file}")
        except subprocess.CalledProcessError as e:
            print(f"Skipping table '{table}' due to error: {e}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "input")
    output_dir = os.path.join(current_dir, "output_mdb")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    mdb_files = glob.glob(os.path.join(input_dir, "*.mdb"))
    if not mdb_files:
        print("No MDB file found in the input folder.")
        return
    extract_tables(mdb_files[0], output_dir)


if __name__ == "__main__":
    main()
