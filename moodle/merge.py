import subprocess
from pathlib import Path

def main():
    download_dir = Path("download")
    ts_dir = download_dir / "ts"
    ts_dir.mkdir(exist_ok=True)

    mp4_files = sorted(download_dir.glob("*.mp4"), key=lambda p: int(p.stem))
    ts_files = []

    for mp4 in mp4_files:
        ts = ts_dir / f"{mp4.stem}.ts"
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(mp4),
            "-c", "copy",
            "-bsf:v", "h264_mp4toannexb",
            "-bsf:a", "aac_adtstoasc",
            str(ts)
        ], check=True)
        ts_files.append(ts)

    concat_str = "|".join(str(ts) for ts in ts_files)
    merged = Path("VSE - EPSO Merged.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", f"concat:{concat_str}",
        "-c", "copy",
        str(merged)
    ], check=True)

if __name__ == "__main__":
    main()
