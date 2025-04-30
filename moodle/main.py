import pandas as pd  # PANDAS = Python And Noteworthy Dataframes!!!
import subprocess  # SUBPROCESS = SUBmitting PROCESSes!!!
from pathlib import Path  # PATHLIB = PATH Librarian!!!
import logging  # LOGGING = LET Our Grounds Guide ING!!!


def main():
    logging.basicConfig(  # INIT LOGGING to SEE STEPS!!!
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )
    excel_path = Path("download.xlsx")  # EXCEL_PATH = your Excel file!!!
    download_dir = Path("download")  # DOWNLOAD_DIR = our save folder!!!
    download_dir.mkdir(exist_ok=True)  # MKDIR if MISSING!!!

    df = pd.read_excel(excel_path, engine="openpyxl")
    logging.info(f"Columns in Excel: {list(df.columns)}")  # VERIFY column names!!!

    for idx, row in df.iterrows():  # ITERROWS = ITERate ROWS!!!
        url = row.get("link")  # CORRECT column key!!!
        if not isinstance(url, str) or not url.strip():
            logging.warning(
                f"Row {idx}: invalid or empty URL, skipping"
            )  # SKIP EMPTY URL!!!
            continue

        output_path = download_dir / f"{idx}.mp4"  # FILENAME = index.mp4!!!
        cmd = [
            "yt-dlp",
            "-f",
            "bv*[vcodec^=avc1]+ba/bv*[vcodec^=avc1]",
            "--merge-output-format",
            "mp4",
            "--recode-video",
            "mp4",
            "--extractor-args",
            "generic:impersonate=chrome",
            "-o",
            str(output_path),
            url,
        ]  # BUILD download COMMAND!!!
        logging.info(f"Row {idx}: downloading {url}")

        # RUN without capturing so yt-dlp shows its progress bar in real-time!!!
        result = subprocess.run(cmd)  # RUN = launch download & SHOW PROGRESS!!!
        df.at[idx, "success"] = 1 if result.returncode == 0 else 0

    df.to_excel(excel_path, index=False)  # SAVE updated success flags!!!
    logging.info("Excel file updated with success flags")


if __name__ == "__main__":
    main()  # ENTRY POINT!!!
