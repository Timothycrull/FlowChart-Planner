"""
The FlowChartMaker class is a Tkinter-based application that allows users to create and save flow charts. It provides a canvas for 
drawing shapes (circles, rectangles, squares, and lines), and allows users to open and save flow chart data to a file.

The class has the following main features:
- A menu bar with options for creating a new file, opening an existing file, saving the current file, and exiting the application.
- A canvas for drawing shapes and lines.
- Buttons for adding different shapes (circle, rectangle, square, and line) to the canvas.
- Functionality for moving and editing the shapes on the canvas.
- Saving and loading flow chart data to/from a text file.
"""
import tkinter as tk
from tkinter import filedialog, simpledialog
import pickle

class FlowChartMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flow Chart Maker")
        self.geometry("800x600")

        # Create a canvas to draw the flow chart
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Bind mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.move_item)
        self.canvas.bind("<Button-1>", self.start_action)
        self.canvas.bind("<ButtonRelease-1>", self.end_action)

        # Shapes list
        self.shapes = []

        # Current line
        self.current_line = None
        self.drawing_line = False

        # Create shape buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side="bottom", fill="x")

        circle_button = tk.Button(button_frame, text="Circle", command=self.add_circle)
        circle_button.pack(side="left", padx=5, pady=5)

        rectangle_button = tk.Button(button_frame, text="Rectangle", command=self.add_rectangle)
        rectangle_button.pack(side="left", padx=5, pady=5)

        square_button = tk.Button(button_frame, text="Square", command=self.add_square)
        square_button.pack(side="left", padx=5, pady=5)

        line_button = tk.Button(button_frame, text="Line", command=self.start_drawing_line)
        line_button.pack(side="left", padx=5, pady=5)

        # Create a menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)

    #Adds a new circle shape to the canvas with the specified text.
    def add_circle(self):
        shape_text = simpledialog.askstring("Circle Text", "Enter text for the circle:")
        if shape_text:
            x, y = self.canvas.winfo_pointerx() - self.winfo_rootx(), self.canvas.winfo_pointery() - self.winfo_rooty()
            r = 30  # Default radius
            shape_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, outline="black")
            text_id = self.canvas.create_text(x, y, text=shape_text)
            self.shapes.append(("oval", shape_id, text_id, shape_text))


    #Adds a new rectangle shape to the canvas with the specified text.
    def add_rectangle(self):
        shape_text = simpledialog.askstring("Rectangle Text", "Enter text for the rectangle:")
        if shape_text:
            x1, y1 = self.canvas.winfo_pointerx() - self.winfo_rootx(), self.canvas.winfo_pointery() - self.winfo_rooty()
            x2, y2 = x1 + 100, y1 + 50  # Default width and height
            shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
            text_id = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=shape_text)
            self.shapes.append(("rectangle", shape_id, text_id, shape_text))


    #Adds a new square shape to the canvas with the specified text. 
    def add_square(self):
        shape_text = simpledialog.askstring("Square Text", "Enter text for the square:")
        if shape_text:
            x1, y1 = self.canvas.winfo_pointerx() - self.winfo_rootx(), self.canvas.winfo_pointery() - self.winfo_rooty()
            side = 50  # Default side length
            x2, y2 = x1 + side, y1 + side
            shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
            text_id = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=shape_text)
            self.shapes.append(("rectangle", shape_id, text_id, shape_text))



    #Starts a new line drawing action on the canvas.
    def start_drawing_line(self):
        self.drawing_line = True

    #Starts a new line drawing action on the canvas.
    def start_action(self, event):
        if event.type == "4" and self.drawing_line and self.current_line is None:
            self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black")
            self.shapes.append(("line", self.current_line))  # Store the line ID as a tuple

    #Updates the coordinates of the current line being drawn on the canvas.
    def draw_line(self, event):
        if self.current_line:
            x, y = event.x, event.y
            coords = self.canvas.coords(self.current_line)
            self.canvas.coords(self.current_line, coords[0], coords[1], x, y)

    #Ends the current line drawing action on the canvas.    
    def end_action(self, event):
        if self.current_line:
            self.current_line = None
            self.drawing_line = False

    #Moves an item (oval, rectangle, or line) on the canvas based on the user's mouse drag event.    
    def move_item(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            tags = self.canvas.gettags(item)
            if "text" not in tags:  # Exclude text items
                x1, y1, x2, y2 = self.canvas.coords(item)
                dx, dy = event.x - (x1 + x2) // 2, event.y - (y1 + y2) // 2
                self.canvas.move(item, dx, dy)
                if "oval" in tags or "rectangle" in tags:
                    for shape_tuple in self.shapes:
                        if shape_tuple[1] == item:
                            text_id = shape_tuple[2]
                            self.canvas.move(text_id, dx, dy)
                            new_x, new_y = (x1 + x2) // 2 + dx, (y1 + y2) // 2 + dy
                            self.canvas.coords(text_id, new_x, new_y)



    #Loads shapes and lines from a file and adds them to the canvas.
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".flowchart")
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    self.shapes = pickle.load(file)
                    self.redraw_shapes()
            except Exception as e:
                print(f"Error opening file: {e}")

    #Saves the shapes and lines drawn on the canvas to a file.
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".flowchart")
        if file_path:
            try:
                with open(file_path, "wb") as file:
                    pickle.dump(self.shapes, file)
            except Exception as e:
                print(f"Error saving file: {e}")


    #Redraws the shapes on the canvas.
    def redraw_shapes(self):
        self.canvas.delete("all")
        for shape_tuple in self.shapes:
            shape_type, shape_id, *args = shape_tuple
            if shape_type == "oval":
                self.canvas.create_oval(self.canvas.coords(shape_id), outline="black")
                text_id, text = args
                self.canvas.create_text(self.canvas.coords(text_id), text=text)
            elif shape_type == "rectangle":
                self.canvas.create_rectangle(self.canvas.coords(shape_id), outline="black")
                text_id, text = args
                self.canvas.create_text(self.canvas.coords(text_id), text=text)
            elif shape_type == "line":
                self.canvas.create_line(self.canvas.coords(shape_id), fill="black")

if __name__ == "__main__":
    app = FlowChartMaker()
    app.mainloop()
