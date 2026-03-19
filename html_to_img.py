import os
import imgkit

INPUT_FOLDER = "output"
IMAGE_OUTPUT = "ticket_images"

WKHTMLTOIMAGE_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe"

config = imgkit.config(wkhtmltoimage=WKHTMLTOIMAGE_PATH)

os.makedirs(IMAGE_OUTPUT, exist_ok=True)

options = {
    "enable-local-file-access": "",
    "quality": "100",

    "width": "800",          # match ticket width
    "disable-smart-width": "",

    "crop-w": "800",         # crop exactly to ticket size
    "crop-h": "500"
}

for file in sorted(os.listdir(INPUT_FOLDER)):

    if file.endswith(".html"):

        html_path = os.path.join(INPUT_FOLDER, file)

        image_name = file.replace(".html", ".png")
        image_path = os.path.join(IMAGE_OUTPUT, image_name)

        imgkit.from_file(
            html_path,
            image_path,
            config=config,
            options=options
        )

        print("Generated:", image_path)