from PIL import Image
import pyheif


def heic_to_jpg(input_path: str, output_path: str):
    heif_file = pyheif.read(input_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    image.save(output_path, "JPEG", quality=100)  # Set quality to maximum


def jpg_to_png(input_path: str, output_path: str, transparent_color=None):
    image = Image.open(input_path).convert("RGBA")
    if transparent_color:
        datas = image.getdata()
        new_data = []
        for item in datas:
            # Make specified color transparent
            if item[:3] == transparent_color:
                new_data.append((255, 255, 255, 0))  # to transparent
            else:
                new_data.append(item)
        image.putdata(new_data)
    image.save(output_path, "PNG")


def png_to_jpg(input_path: str, output_path: str):
    image = Image.open(input_path).convert("RGB")
    image.save(output_path, "JPEG", quality=100)  # Set quality to maximum
