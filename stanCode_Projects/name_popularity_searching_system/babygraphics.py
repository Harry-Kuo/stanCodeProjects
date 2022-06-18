"""
File: babygraphics.py
Name: Harry Kuo
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    interval = (width - GRAPH_MARGIN_SIZE*2) / len(YEARS)   # to calculate the average distance between the years
    x = GRAPH_MARGIN_SIZE + interval * year_index
    return x


def get_y_coordinate(height, rank):
    interval = (height - GRAPH_MARGIN_SIZE*2) / 1000        # to calculate the average distance between the ranks
    y = GRAPH_MARGIN_SIZE + interval * rank
    return y


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    # to draw two horizontal lines of boundaries
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)

    # to draw the vertical lines according to the 'YEARS' list
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), GRAPH_MARGIN_SIZE, get_x_coordinate(CANVAS_WIDTH, i),
                           CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=str(YEARS[i]),
                           anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #

    temp = {}
    temp_value = {}
    for name_to_check in lookup_names:
        temp[name_to_check] = []            # to store y-coordinate
        temp_value[name_to_check] = []      # to store rank
        for i in range(len(YEARS)):
            if str(YEARS[i]) in name_data[name_to_check]:
                value = int(name_data[name_to_check][str(YEARS[i])])
                temp_value[name_to_check].append(str(value))
            else:
                value = 1000
                temp_value[name_to_check].append('*')

            y1 = get_y_coordinate(CANVAS_HEIGHT, value)
            x1 = get_x_coordinate(CANVAS_WIDTH, i)
            temp[name_to_check].append(x1)
            temp[name_to_check].append(y1)

    name_count = 0
    for name in temp:
        color = name_count % 4              # to determine the index in COLORS
        # to plot the baby name data
        for i in range(0, len(temp[name])-3, 2):
            canvas.create_line(temp[name][i], temp[name][i+1], temp[name][i+2], temp[name][i+3], fill=COLORS[color])
        # to add the text near the baby name data coordinate
        for i in range(0, len(temp[name]), 2):
            canvas.create_text(temp[name][i]+TEXT_DX, temp[name][i+1], text=name+" "+temp_value[name][int(i/2)],
                               anchor=tkinter.SW, fill=COLORS[color])
        name_count += 1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
