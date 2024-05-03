from tkinter import *
import tkinter.ttk as ttk
from tkinter import colorchooser
from tkinter import filedialog  
from PIL import Image, ImageDraw, ImageFilter, ImageGrab, ImageTk
import PIL
from tkinter import messagebox 
import math
import random

root = Tk() 
root.title('Paint Program')
root.geometry("800x800")

brush_colour = "black"

def paint(event):
    brush_width = '%0.0f'% float(my_slider.get())
    brush_type2 = brush_type.get()
    
    if brush_type2 == "fan":
        draw_fan(event)
    elif brush_type2 == "oil":
        draw_oil_brush(event, brush_width)
    elif brush_type2 == "watercolor":
        draw_watercolor_brush(event, brush_width)
    elif brush_type2 == "smudge":
        smudge(event)
    else:
        draw_brush(event, brush_width, brush_type2)

def draw_brush(event, brush_width, brush_type2):
    x1 = event.x - 1
    y1 = event.y - 1
    x2 = event.x + 1
    y2 = event.y + 1
    my_canvas.create_line(x1, y1, x2, y2, fill=brush_colour, width=brush_width, capstyle=brush_type2, smooth=True)

def draw_fan(event):
    num_lines = 10  # Number of lines to draw
    radius = 30  # Radius of the fan
    center_x = event.x
    center_y = event.y

    for angle in range(180, 360, int(180 / num_lines)):  # Draw only for the bottom half (180 to 360 degrees)
        end_x = center_x + radius * math.cos(math.radians(angle))
        end_y = center_y + radius * math.sin(math.radians(angle))
        my_canvas.create_line(center_x, center_y, end_x, end_y, fill=brush_colour, width=my_slider.get())

def draw_oil_brush(event, brush_width):
    radius = int(brush_width) // 2
    center_x = event.x
    center_y = event.y
    num_strokes = 10  # Number of oil paint strokes
    
    for _ in range(num_strokes):
        rand_x = random.randint(center_x - radius, center_x + radius)
        rand_y = random.randint(center_y - radius, center_y + radius)
        brush_color = generate_random_color()  # Generate random color for each stroke
        my_canvas.create_oval(rand_x - radius, rand_y - radius, rand_x + radius, rand_y + radius, fill=brush_color, outline="")

def draw_watercolor_brush(event, brush_width):
    x1 = event.x - 10
    y1 = event.y - 10
    x2 = event.x + 10
    y2 = event.y + 10
    my_canvas.create_oval(x1, y1, x2, y2, fill=brush_colour, outline="", width=brush_width)

def smudge(event):
    brush_size = int(my_slider.get())
    x = event.x
    y = event.y
    x1 = x - brush_size
    y1 = y - brush_size
    x2 = x + brush_size
    y2 = y + brush_size
    
    # Get the region to be smudged
    region = my_canvas.find_enclosed(x1, y1, x2, y2)
    
    # Smudge each object in the region
    for item in region:
        # Smudge only lines (brush strokes)
        if my_canvas.type(item) == "line":
            coords = my_canvas.coords(item)
            smudge_line(coords)
    

def smudge_line(coords):
    # Calculate the average of consecutive points to create the smudge effect
    for i in range(len(coords) - 2):
        x1, y1 = coords[i], coords[i + 1]
        x2, y2 = coords[i + 2], coords[i + 3]
        avg_x = (x1 + x2) / 2
        avg_y = (y1 + y2) / 2
        
        # Move the points slightly towards the average
        my_canvas.coords(item, x1, y1, avg_x, avg_y)

def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def change_brush_size(event):
    slider_label.config(text='%0.0f'% float(my_slider.get()))

def change_brush_colour():
    global brush_colour
    brush_colour = "black"
    brush_colour = colorchooser.askcolor(color=brush_colour)[1]

def change_canvas_colour():
    global bg_colour
    bg_colour = "black"
    bg_colour = colorchooser.askcolor(color=bg_colour)[1]
    my_canvas.config(bg=bg_colour)

def clear_screen():
    my_canvas.delete(ALL)
    my_canvas.config(bg="white")

def save_as_png():
    result = filedialog.asksaveasfilename(initialdir="c:/paint", filetypes=(("png files", ".png"), ("all files", ".*")))
    if result.endswith('.png'):
        pass
    else:
        result = result + '.png' 

    if result:
        x = root.winfo_rootx() + my_canvas.winfo_x()
        y = root.winfo_rooty() + my_canvas.winfo_y()
        x1 = x + my_canvas.winfo_width()
        y1 = y + my_canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(result)
        messagebox.showinfo("Image Saved", "Your image has been saved!")

w = 600
h = 400

my_canvas = Canvas(root, width=w, height=h, bg="white")
my_canvas.pack(pady=20)
my_canvas.bind('<B1-Motion>', paint)

# Create a blank white image for smudging
blurred = Image.new('RGBA', (w, h), (255, 255, 255, 255))

brush_options_frame = Frame(root)
brush_options_frame.pack(pady=20)

brush_size_frame = LabelFrame(brush_options_frame, text="Brush Size")
brush_size_frame.grid(row=0, column=0, padx=50)

my_slider = ttk.Scale(brush_size_frame, from_=1, to=100, command=change_brush_size, orient=VERTICAL, value=1)
my_slider.pack(pady=10, padx=10)

slider_label = Label(brush_size_frame, text=my_slider.get())
slider_label.pack(pady=5)

brush_type_frame = LabelFrame(brush_options_frame, text="Brush Type", height=400)
brush_type_frame.grid(row=0, column=1, padx=50)

brush_type = StringVar()
brush_type.set("round")

brush_type_radio1 = Radiobutton(brush_type_frame, text="Round", variable=brush_type, value="round")
brush_type_radio2 = Radiobutton(brush_type_frame, text="Slash", variable=brush_type, value="butt")
brush_type_radio3 = Radiobutton(brush_type_frame, text="Diamond", variable=brush_type, value="projecting")
brush_type_radio4 = Radiobutton(brush_type_frame, text="Fan", variable=brush_type, value="fan")
brush_type_radio5 = Radiobutton(brush_type_frame, text="Oil Brush", variable=brush_type, value="oil")
brush_type_radio6 = Radiobutton(brush_type_frame, text="Watercolor", variable=brush_type, value="watercolor")
brush_type_radio7 = Radiobutton(brush_type_frame, text="Smudge", variable=brush_type, value="smudge")

brush_type_radio1.pack(anchor=W)
brush_type_radio2.pack(anchor=W)
brush_type_radio3.pack(anchor=W)
brush_type_radio4.pack(anchor=W)
brush_type_radio5.pack(anchor=W)
brush_type_radio6.pack(anchor=W)
brush_type_radio7.pack(anchor=W)

change_colours_frame = LabelFrame(brush_options_frame, text="Change Colours")
change_colours_frame.grid(row=0, column=2) 

brush_colour_button = Button(change_colours_frame, text="Brush Colour", command=change_brush_colour)
brush_colour_button.pack(pady=10, padx=10)

canvas_colour_button = Button(change_colours_frame, text="Canvas Colour", command=change_canvas_colour)
canvas_colour_button.pack(pady=10, padx=10)


options_frame = LabelFrame(brush_options_frame, text="Program Options")
options_frame.grid(row=0, column=3, padx=50)

clear_button = Button(options_frame, text="Clear Screen", command=clear_screen)
clear_button.pack(padx=10, pady=10)

save_image_button = Button(options_frame, text="Save to PNG", command=save_as_png)
save_image_button.pack(padx=10, pady=10)

root.mainloop()