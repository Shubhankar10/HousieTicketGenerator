import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROWS = 3
COLS = 9

column_ranges = [
    (1, 9),
    (10, 19),
    (20, 29),
    (30, 39),
    (40, 49),
    (50, 59),
    (60, 69),
    (70, 79),
    (80, 90)
]


def generate_ticket():
    """
    Generate a valid tambola ticket
    """
    ticket = [[None for _ in range(COLS)] for _ in range(ROWS)]

    # choose columns where numbers will exist in each row
    row_positions = []
    for _ in range(ROWS):
        cols = sorted(random.sample(range(COLS), 5))
        row_positions.append(cols)

    # fill numbers
    column_numbers = {}

    for col in range(COLS):
        start, end = column_ranges[col]
        count = sum(col in row_positions[r] for r in range(ROWS))

        if count > 0:
            nums = random.sample(range(start, end + 1), count)
            nums.sort()
            column_numbers[col] = nums

    # place numbers into ticket
    for col, nums in column_numbers.items():
        i = 0
        for r in range(ROWS):
            if col in row_positions[r]:
                ticket[r][col] = nums[i]
                i += 1

    return ticket


def draw_ticket(c, ticket, x, y):
    """
    Draw one ticket grid on canvas
    """
    cell_w = 25
    cell_h = 25

    for r in range(ROWS):
        for col in range(COLS):

            xpos = x + col * cell_w
            ypos = y - r * cell_h

            c.rect(xpos, ypos, cell_w, cell_h)

            val = ticket[r][col]
            if val:
                c.drawCentredString(
                    xpos + cell_w/2,
                    ypos + cell_h/2 - 4,
                    str(val)
                )


def generate_pdf(num_tickets=12):

    c = canvas.Canvas("tickets.pdf", pagesize=A4)

    width, height = A4

    tickets_per_page = 6
    margin_x = 40
    margin_y = height - 80

    spacing_x = 260
    spacing_y = 120

    for i in range(num_tickets):

        if i % tickets_per_page == 0 and i != 0:
            c.showPage()

        ticket = generate_ticket()

        pos = i % tickets_per_page
        row = pos // 2
        col = pos % 2

        x = margin_x + col * spacing_x
        y = margin_y - row * spacing_y

        c.drawString(x, y + 20, f"Ticket #{i+1}")

        draw_ticket(c, ticket, x, y)

    c.save()
    print("PDF generated: tickets.pdf")


if __name__ == "__main__":
    generate_pdf(30)