import tkinter
import time
import math
from Line import Line
from Curve import Curve


# Create the main window of the animation
def create_animation_window():
    window = tkinter.Tk()
    window.title("Lissajous Table Animation")
    window.attributes("-fullscreen", True)
    return window


# Create a canvas for animation and add it to main window
def create_animation_canvas(window, background):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg=background)
    canvas.pack(fill="both", expand=True)
    return canvas


# Create and animate Lissajous table
def draw(
    window, canvas, width, speed, colours, bgColour, ncColour, linetoggle, end=None
):
    start = time.time()
    buffer = 5
    rows = int(animation_window_height / width)
    cols = int(animation_window_width / width)
    angle = math.radians(0)
    r = (width - (2 * buffer)) / 2
    x = r * math.sin(angle)
    y = r * math.cos(angle)
    lines = [[], []]
    curves = []

    # For each column
    for i in range(1, cols):
        # create a guide circle
        canvas.create_oval(
            i * width + buffer,
            buffer,
            i * width + width - buffer,
            width - buffer,
            outline=ncColour,
        )
        # Create guide point and if specified line
        if linetoggle == 0:
            lines[0].append(
                (
                    Line(
                        i * width + (width / 2) - x,
                        0 - 2 * width,
                        i * width + (width / 2) - x,
                        animation_window_height + 2 * width,
                        i * speed,
                        canvas,
                        bgColour,
                    ),
                    canvas.create_oval(
                        i * width + (width / 2) - x,
                        buffer,
                        i * width + (width / 2) - x,
                        buffer,
                        width=5,
                        outline=ncColour,
                    ),
                )
            )
        else:
            lines[0].append(
                (
                    Line(
                        i * width + (width / 2) - x,
                        0 - 2 * width,
                        i * width + (width / 2) - x,
                        animation_window_height + 2 * width,
                        i * speed,
                        canvas,
                        ncColour,
                    ),
                    canvas.create_oval(
                        i * width + (width / 2) - x,
                        buffer,
                        i * width + (width / 2) - x,
                        buffer,
                        width=5,
                        outline=ncColour,
                    ),
                )
            )

    # For each row
    for i in range(1, rows):
        # create a guide circle
        canvas.create_oval(
            buffer,
            i * width + buffer,
            width - buffer,
            i * width + width - buffer,
            outline=ncColour,
        )
        # Create guide point and if specified line
        if linetoggle == 0:
            lines[1].append(
                (
                    Line(
                        0 - 2 * width,
                        i * width + (width / 2) - y,
                        animation_window_width + 2 * width,
                        i * width + (width / 2) - y,
                        i * speed,
                        canvas,
                        bgColour,
                    ),
                    canvas.create_oval(
                        width / 2,
                        i * width + (width / 2) - y,
                        width / 2,
                        i * width + (width / 2) - y,
                        width=5,
                        outline=ncColour,
                    ),
                )
            )
        else:
            lines[1].append(
                (
                    Line(
                        0 - 2 * width,
                        i * width + (width / 2) - y,
                        animation_window_width + 2 * width,
                        i * width + (width / 2) - y,
                        i * speed,
                        canvas,
                        ncColour,
                    ),
                    canvas.create_oval(
                        width / 2,
                        i * width + (width / 2) - y,
                        width / 2,
                        i * width + (width / 2) - y,
                        width=5,
                        outline=ncColour,
                    ),
                )
            )

    # Initialise a curve for each row, column space
    for i in range(rows - 1):
        curves.append([])
        for j in range(cols - 1):
            curves[i].append(Curve())

    # Create statistic texts
    canvas.create_text(5, 5, text=f"Width: {str(width)}px", fill=ncColour, anchor="nw")
    canvas.create_text(5, 15, text=f"Cols: {str(cols-1)}", fill=ncColour, anchor="nw")
    canvas.create_text(5, 25, text=f"Rows: {str(rows-1)}", fill=ncColour, anchor="nw")
    canvas.create_text(5, 35, text=f"Speed: {str(speed)}", fill=ncColour, anchor="nw")

    if not end == None:
        canvas.create_text(
            5,
            45,
            text=f"Previous Time: {str(round(end))}s",
            fill=ncColour,
            anchor="nw",
            width=width,
        )

    # Main Loop
    while True:

        # For each curve
        for i in range(len(lines[0])):
            for j in range(len(lines[1])):
                # store the current point then draw
                curves[j][i].add_point(lines[0][i][0].comp(lines[1][j][0], canvas))

                # Try except used as curve cant be drawn until there is more than 1 point
                try:
                    curves[j][i].draw(canvas, colours)
                except:
                    pass

        # For each vertical line
        for i in range(len(lines[0])):
            # Store current point
            px, py = r * math.sin(lines[0][i][0].angle), r * math.cos(
                lines[0][i][0].angle
            )

            # Update the line
            lines[0][i][0].update()

            # Store the next point
            x, y = r * math.sin(lines[0][i][0].angle), r * math.cos(
                lines[0][i][0].angle
            )

            # Move the guide point and line by the difference between current and next point
            canvas.move(lines[0][i][0].line, px - x, py - y)
            canvas.move(lines[0][i][1], px - x, py - y)

        # For each horizontal line
        for i in range(len(lines[1])):
            # Store current point
            px, py = r * math.sin(lines[1][i][0].angle), r * math.cos(
                lines[1][i][0].angle
            )

            # Update the line
            lines[1][i][0].update()

            # Store the next point
            x, y = r * math.sin(lines[1][i][0].angle), r * math.cos(
                lines[1][i][0].angle
            )

            # Move the guide point and line by the difference between current and next point
            canvas.move(lines[1][i][0].line, px - x, py - y)
            canvas.move(lines[1][i][1], px - x, py - y)

        # Once a full rotation has been made (eg animation complete)
        if lines[0][0][0].angle > 6.3:

            # Calculate time to complete
            end = time.time() - start

            # Pause the program
            time.sleep(3)

            # Clear canvas and recall draw method
            canvas.delete("all")
            draw(
                animation_window,
                animation_canvas,
                width,
                speed,
                colours,
                bgColour,
                ncColour,
                linetoggle,
                end,
            )

        window.update()


# toggle lines (0 or 1)
linetoggle = 1

# width of area for each curve (smaller width -> more curves -> runs slower)
width = 100

# speed of rotation (in radians)
speed = 0.8

# sample colours: "red", "orange", "yellow", "green", "blue", "purple", "pink", "white"
# colour of curves (can choose multiple and curve will choose randomly)
curveColours = ["turquoise1"]
# colour of background
bgColour = "turquoise4"
# colour of edge circles and guide lines
guideColour = "turquoise3"


# Initialise animation window and canvas
animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window, bgColour)

# Get window width and height
animation_window_width = animation_window.winfo_screenwidth()
animation_window_height = animation_window.winfo_screenheight()

# Start the draw method
draw(
    animation_window,
    animation_canvas,
    width,
    speed,
    curveColours,
    bgColour,
    guideColour,
    linetoggle,
)
