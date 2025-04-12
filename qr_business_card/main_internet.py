import qrcode
import datetime
import os

output_folder = "output_internet"
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
profile_picture_url = "https://avatars.githubusercontent.com/u/154789069?s=400&u=9f5d0ab3a0adfd1ffca90044bba02442744a062e&v=4"  # UPDATE with your hosted image URL

notes = "Experienced procurement specialist in welding and materials testing."

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
PHOTO;VALUE=URI:{profile_picture_url}
END:VCARD
"""

qr = qrcode.QRCode(
    version=40,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(vcard_data)
qr.make(fit=True)

now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
vcard_filename = f"{first_name}_{last_name}_{now}_internet.png"
output_path = os.path.join(output_folder, vcard_filename)
img_qr = qr.make_image(fill="black", back_color="white")
img_qr.save(output_path)

print(f"✅ QR Code generated and saved at: {output_path}")