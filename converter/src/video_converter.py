import ffmpeg

def mov_to_mp4(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(
        output_path,
        vcodec='libx264',
        preset='slow',
        crf=18,
        acodec='aac',
        threads=1
    ).run()

def mp4_to_mov(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(
        output_path,
        vcodec='prores',
        qscale=0,
        threads=1
    ).run()

def video_to_gif(input_path: str, output_path: str):
    ffmpeg.input(input_path).filter('fps', fps=10).output(
        output_path,
        threads=1
    ).run()

def gif_to_video(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(
        output_path,
        vcodec='libx264',
        preset='slow',
        crf=18,
        threads=1
    ).run()

def live_photo_to_gif(input_path: str, output_path: str):
    ffmpeg.input(input_path).filter('fps', fps=10).output(
        output_path,
        threads=1
    ).run()

def live_photo_to_video(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(
        output_path,
        vcodec='libx264',
        threads=1
    ).run()