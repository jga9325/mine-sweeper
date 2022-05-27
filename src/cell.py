from tkinter import Button, Label
import random
import settings
import ctypes
import sys

# Cell class represents a cell on the mine sweeper board
# Each cell has a button so it can be clicked
class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.has_been_clicked = False

        # Append the object to the Cell.all list
        Cell.all.append(self)

     # Represents a list of cell objects that surround the cell
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1),
            self.get_cell_by_axis(self.x, self.y+1),
        ]
        
        cells = [cell for cell in cells if cell != None]
        return cells

    # Represents a count of mines around the cell
    @property
    def surrounded_cells_mine_count(self):
        count = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                count += 1
        return count

    # Create a new button object for this cell and bind clicks to actions
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
            bg="#AFAFAF"
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    # Create a label for the count of cells left when playing the game
    # It is static because it is a count for all of the cells not just one instance
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"Cells Left: {Cell.cell_count}",
            bg="black",
            fg="#AFAFAF",
            font=("", 24)
        )
        Cell.cell_count_label_object = lbl

    # Handle left clicks
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mine_count == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If the number of mines left is the same as the number of cells left,
            # then the player wins
            if Cell.cell_count == settings.MINES_COUNT:  
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations, you won the game!', 'Game Over', 0)
                sys.exit()
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    # Return a cell object by providing its coordinates
    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    # Functionality for if a cell is left clicked
    def show_cell(self):
        if not self.has_been_clicked:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text = self.surrounded_cells_mine_count)
            # Update cell count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left: {Cell.cell_count}"
                )
            # Set original background color in case orange cell was clicked
            self.cell_btn_object.configure(
                bg="SystemButtonFace"
            )
        self.has_been_clicked = True

    # Functionality for right clicks
    def show_mine(self):
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()

    # Handles right clicks
    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg="orange"
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg="#AFAFAF"
            )
            self.is_mine_candidate = False

    # Chooses random cells to be mines
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    # Returns a string version of the Cell class with its x and y coordinates
    def  __repr__(self):
        return f"Cell({self.x}, {self.y})"