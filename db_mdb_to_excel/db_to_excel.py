import sqlite3
import pandas as pd
import os
import glob


def extract_tables(db_path: str, output_dir: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        try:
            df = pd.read_sql_query(f"SELECT * FROM '{table}';", conn)
            excel_file = os.path.join(output_dir, f"{table}.xlsx")
            df.to_excel(excel_file, index=False)
            print(f"Exported table '{table}' to {excel_file}")
        except Exception as e:
            print(f"Skipping table '{table}' due to error: {e}")
    cursor.close()
    conn.close()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "input")
    output_dir = os.path.join(current_dir, "output_DB")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    db_files = glob.glob(os.path.join(input_dir, "*.db"))
    if not db_files:
        print("No DB file found in the input folder.")
        return
    extract_tables(db_files[0], output_dir)


if __name__ == "__main__":
    main()
