import os
from PIL import Image

INPUT_FOLDER = "ticket_images"
OUTPUT_FILE = "tickets_print.pdf"

# A4 size at 300 DPI
A4_WIDTH = 2480
A4_HEIGHT = 3508

# Ticket size (scaled slightly to fit)
TICKET_WIDTH = 1772
TICKET_HEIGHT = 1100

# 1 cm padding at 300 DPI
PADDING_Y = 50

ROWS = 3

images = []

for file in sorted(os.listdir(INPUT_FOLDER)):
    if file.endswith(".png"):
        images.append(os.path.join(INPUT_FOLDER, file))

pages = []

for i in range(0, len(images), ROWS):

    page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    batch = images[i:i + ROWS]

    for index, img_path in enumerate(batch):

        img = Image.open(img_path)
        img = img.resize((TICKET_WIDTH, TICKET_HEIGHT))

        # center horizontally
        x = (A4_WIDTH - TICKET_WIDTH) // 2

        y = index * (TICKET_HEIGHT + PADDING_Y) + 100

        page.paste(img, (x, y))

    pages.append(page)


pages[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=pages[1:]
)

print("PDF created:", OUTPUT_FILE)