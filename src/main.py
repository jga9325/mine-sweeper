from tkinter import *
import settings
import utils
from cell import Cell
from PIL import Image, ImageTk

root = Tk()

# Override the default settings of the window
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Mine Sweeper")
root.resizable(False, False)

# Create a frame to hold the title
top_frame = Frame(
    root,
    bg="black",
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
top_frame.place(x=0, y=0)

# Create a title for the game
game_title = Label(
    top_frame,
    bg="#00387A",
    fg="white",
    text="Mine Sweeper",
    font=("", 42),
    width=15
)
game_title.place(x=utils.width_prct(40.5),y=40)

# Create a frame to hold game info and directions
left_frame = Frame(
    root,
    bg="black",
    width=utils.width_prct(36),
    height=utils.height_prct(75)
)
left_frame.place(x=0, y=utils.height_prct(25))

# Create a frame to hold the board
center_frame = Frame(
    root,
    bg="black",
    width=utils.width_prct(75),
    height=utils.height_prct(75)
)
center_frame.place(
    x=utils.width_prct(37),
    y=utils.height_prct(25)
)

# Create the board and place it in the center frame
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x, row=y
        )

# Create a new label in the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=85, y=0)

# Create a new label to display the total number of mines
mines_count_display = Label(
    left_frame,
    bg="black",
    fg="#9E0000",
    text=f"Total Mines: {settings.MINES_COUNT}",
    font=("", 24)
)
mines_count_display.place(x=80, y=60)

# Add a label for the directions title
directions_title = Label(
    left_frame,
    fg="white",
    bg="black",
    text="Directions",
    font=("", 20, "underline")
)
directions_title.place(x=120, y=120)

# Add a label for the directions text
directions = Label(
    left_frame,
    bg="black",
    fg="white",
    text="""- Left click on a cell to reveal the number of\nmines around it (on all sides including\ndiagonally)\n
- If you left click on a mine, you lose\n
- Right click on a cell that you think is a mine to\nmark it orange\n
- Click on all of the cells that are not mines in\norder to win the game\n
- Good Luck!""",
    font=("", 13),
    justify="center"
)
directions.place(x=5, y=170)

# Open image and resize it
image = Image.open("src/explosion.png")
resized_image = image.resize((150, 150), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)

# Create a new label to place the image in the top frame
pic = Label(
    top_frame,
    image=new_image,
    width=150,
    height=150,
    bg="black"
)
pic.place(x=102, y=10)

# Set random cells to become mines
Cell.randomize_mines()

# Run the window
root.mainloop()