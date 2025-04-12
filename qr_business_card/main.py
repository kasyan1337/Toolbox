import qrcode
import datetime
import os
import base64
from PIL import Image
import io

output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

first_name = "Kasim"
last_name = "Janči"
title = "MPhil."
formatted_name = f"{title} {first_name} {last_name}"

company = "Welding & Testing of Materials s.r.o."
job_title = "Procurement Manager"

phone_work = "+421 944 118 730"
phone_mobile = "+421 944 118 730"
phone_home = "+421 944 118 730"
phone_fax = "+421 944 118 730"

email_work = "kjanci@wtm.sk"
email_personal = "kasim.janci@gmail.com"

website = "https://www.wtm.sk"
linkedin = "https://www.linkedin.com/in/kasimjanci"
twitter = "https://twitter.com/kasim"

street = "Dlhá 1011/88D"
city = "Žilina"
region = ""
postal_code = "01009"
country = "Slovakia"

birthday = "1998-10-08"
profile_picture_path = "images/photo_sjtu.png"

notes = "Experienced procurement specialist in welding and materials testing."

def compress_image_to_target(image_path, max_bytes=800):
    try:
        img = Image.open(image_path)
        img.thumbnail((150, 150))  # RESIZE IMAGE TO MAX 150x150 (MAINTAINS ASPECT RATIO)
        # TRY DIFFERENT QUALITY LEVELS TO REDUCE SIZE
        for quality in [50, 40, 30, 20, 10]:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            if len(encoded) <= max_bytes:
                return encoded  # RETURN THE ENCODED IMAGE IF IT FITS THE TARGET SIZE!
        print("⚠️ Compressed image is still too large, skipping image embedding.")
        return None
    except FileNotFoundError:
        print("⚠️ Profile picture not found. Skipping image embedding.")
        return None

profile_picture_base64 = compress_image_to_target(profile_picture_path)

vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name};;{title};
FN:{formatted_name}
ORG:{company}
TITLE:{job_title}
TEL;WORK:{phone_work}
TEL;CELL:{phone_mobile}
TEL;HOME:{phone_home}
TEL;FAX:{phone_fax}
EMAIL;WORK:{email_work}
EMAIL;HOME:{email_personal}
URL:{website}
URL;LinkedIn:{linkedin}
URL;Twitter:{twitter}
ADR;WORK:;;{street};{city};{region};{postal_code};{country}
BDAY:{birthday}
NOTE:{notes}
"""

if profile_picture_base64:
    vcard_data += f"PHOTO;ENCODING=b;TYPE=JPEG:{profile_picture_base64}\n"

vcard_data += "END:VCARD"

qr = qrcode.QRCode(
    version=40,  # FIXED TO VERSION 40, THE MAXIMUM ALLOWED
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # LOW ERROR CORRECTION FOR MAX CAPACITY
    box_size=10,
    border=4,
)

qr.add_data(vcard_data)
qr.make(fit=True)  # GENERATE THE BEST FIT, NOW THAT DATA IS SMALLER

now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
vcard_filename = f"{first_name}_{last_name}_{now}.png"
output_path = os.path.join(output_folder, vcard_filename)
img_qr = qr.make_image(fill="black", back_color="white")
img_qr.save(output_path)

print(f"✅ QR Code generated and saved at: {output_path}")