import random
import os
from jinja2 import Template

# -----------------------
# CONFIGURATION
# -----------------------

VARIATIONS = 180   # change this to generate more

# IMAGE_PATH = "backgroundNoSplash.png"   # placeholder
IMAGE_PATH = "backgroundGulal.png"   # placeholder

TABLE_X = 150
TABLE_Y = 180

OUTPUT_FOLDER = "output"

ROWS = 3
COLS = 9

column_ranges = [
    (1,9),
    (10,19),
    (20,29),
    (30,39),
    (40,49),
    (50,59),
    (60,69),
    (70,79),
    (80,90)
]


# -----------------------
# TICKET GENERATOR
# -----------------------

def generate_ticket():

    ticket = [[None]*COLS for _ in range(ROWS)]

    row_positions = []

    for _ in range(ROWS):
        cols = sorted(random.sample(range(COLS),5))
        row_positions.append(cols)

    column_numbers = {}

    for col in range(COLS):

        start,end = column_ranges[col]

        count = sum(col in row_positions[r] for r in range(ROWS))

        if count > 0:

            nums = random.sample(range(start,end+1),count)
            nums.sort()

            column_numbers[col] = nums

    for col,nums in column_numbers.items():

        i=0

        for r in range(ROWS):

            if col in row_positions[r]:

                ticket[r][col] = nums[i]
                i+=1

    return ticket


# -----------------------
# LOAD HTML TEMPLATE
# -----------------------

with open("template.html") as f:
    template = Template(f.read())


# -----------------------
# GENERATE HTML FILES
# -----------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for i in range(VARIATIONS):

    ticket = generate_ticket()

    html = template.render(
        ticket=ticket,
        image_path=IMAGE_PATH,
        table_x=TABLE_X,
        table_y=TABLE_Y
    )

    output_file = f"{OUTPUT_FOLDER}/ticket_{i+1}.html"

    with open(output_file, "w") as f:
        f.write(html)


    # --------------------------------
    # IMAGE / PDF EXPORT (DISABLED)
    # --------------------------------

    # import imgkit
    # imgkit.from_file(output_file, f"{OUTPUT_FOLDER}/ticket_{i+1}.png")

print(f"{VARIATIONS} HTML tickets generated in '{OUTPUT_FOLDER}' folder.")